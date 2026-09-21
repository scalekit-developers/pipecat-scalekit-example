"""Pipecat voice bot that lists Google Calendar through Scalekit.

The LLM never sees an OAuth token. Scalekit execute_tool runs as TEST_IDENTIFIER.
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame, TTSSpeakFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.worker import PipelineParams, PipelineWorker, ProcessorUnusablePolicy
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.llm_service import FunctionCallParams
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.daily.transport import DailyParams
from pipecat.transports.websocket.fastapi import FastAPIWebsocketParams
from pipecat.workers.runner import WorkerRunner

from scalekit_calendar import list_calendar_events

load_dotenv(override=True)


def _env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


class GatewayLLMService(OpenAILLMService):
    """OpenAI-compatible LLM that may not accept the developer role."""

    supports_developer_role = False


def _llm_service() -> OpenAILLMService:
    openai_key = _env("OPENAI_API_KEY")
    if not openai_key:
        raise RuntimeError("Missing OPENAI_API_KEY.")
    base_url = _env("OPENAI_BASE_URL") or None
    model = _env("OPENAI_MODEL") or ("claude-haiku-4-5" if base_url else "gpt-4o-mini")
    settings = OpenAILLMService.Settings(
        model=model,
        system_instruction=(
            "You are a helpful voice assistant. You can check the user's "
            "Google Calendar through Scalekit using googlecalendar_list_events. "
            "Default calendar_id to primary. When the user asks about today or "
            "this week, pass RFC3339 time_min and time_max. Keep replies short "
            "and spoken. No emojis or bullet lists."
        ),
    )
    logger.info(f"LLM: {model} base_url={base_url or 'openai'}")
    if base_url:
        return GatewayLLMService(api_key=openai_key, base_url=base_url, settings=settings)
    return OpenAILLMService(api_key=openai_key, settings=settings)


def _speech_services():
    """Cloud speech when keys exist. Else local Whisper + Kokoro."""
    deepgram_key = _env("DEEPGRAM_API_KEY")
    cartesia_key = _env("CARTESIA_API_KEY")
    openai_key = _env("OPENAI_API_KEY")
    openai_base = _env("OPENAI_BASE_URL")

    if deepgram_key and cartesia_key:
        from pipecat.services.cartesia.tts import CartesiaTTSService
        from pipecat.services.deepgram.stt import DeepgramSTTService

        stt = DeepgramSTTService(api_key=deepgram_key)
        tts = CartesiaTTSService(
            api_key=cartesia_key,
            settings=CartesiaTTSService.Settings(
                voice=_env("CARTESIA_VOICE_ID") or "71a7ad14-091c-4e8e-a314-022ece01c121",
            ),
        )
        logger.info("Speech: Deepgram STT + Cartesia TTS")
        return stt, tts

    # Real OpenAI speech only. A Scalekit LLM gateway key cannot do Whisper/TTS.
    if openai_key and not openai_base:
        from pipecat.services.openai.stt import OpenAISTTService
        from pipecat.services.openai.tts import OpenAITTSService

        stt = OpenAISTTService(api_key=openai_key)
        tts = OpenAITTSService(api_key=openai_key)
        logger.info("Speech: OpenAI STT + OpenAI TTS")
        return stt, tts

    from pipecat.services.kokoro.tts import KokoroTTSService
    from pipecat.services.whisper.stt import WhisperSTTServiceMLX

    stt = WhisperSTTServiceMLX()
    tts = KokoroTTSService()
    logger.info("Speech: local Whisper STT + Kokoro TTS")
    return stt, tts


async def googlecalendar_list_events(
    params: FunctionCallParams,
    calendar_id: str = "primary",
    time_min: str = "",
    time_max: str = "",
    max_results: int = 10,
):
    """List events from the user's Google Calendar via Scalekit.

    Use this whenever the user asks about their calendar, schedule,
    meetings, or upcoming events.

    Args:
        calendar_id: Calendar to read. Defaults to "primary".
        time_min: Lower bound for event start (RFC3339). Use for "today" or "this week".
        time_max: Upper bound for event start (RFC3339).
        max_results: Maximum events to return. Defaults to 10.
    """
    result = await asyncio.to_thread(
        list_calendar_events,
        identifier=_env("TEST_IDENTIFIER"),
        connection_name=_env("SCALEKIT_CONNECTION_NAME") or "googlecalendar",
        calendar_id=calendar_id,
        time_min=time_min,
        time_max=time_max,
        max_results=max_results,
    )
    if "error" in result:
        logger.error("Scalekit calendar tool failed: {}", result["error"])
    await params.result_callback(result)


transport_params = {
    "daily": lambda: DailyParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
    ),
    "twilio": lambda: FastAPIWebsocketParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
    ),
    "webrtc": lambda: TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
    ),
}


async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    logger.info("Starting Scalekit × Pipecat bot")

    stt, tts = _speech_services()
    llm = _llm_service()

    @llm.event_handler("on_function_calls_started")
    async def on_function_calls_started(service, function_calls):
        await tts.queue_frame(TTSSpeakFrame("Let me check your calendar."))

    context = LLMContext(tools=[googlecalendar_list_events])
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(vad_analyzer=SileroVADAnalyzer()),
    )

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            user_aggregator,
            llm,
            tts,
            transport.output(),
            assistant_aggregator,
        ]
    )

    worker = PipelineWorker(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
        idle_timeout_secs=runner_args.pipeline_idle_timeout_secs,
        processor_unusable_policy=ProcessorUnusablePolicy.END,
    )
    runner = WorkerRunner(handle_sigint=runner_args.handle_sigint)
    await runner.add_workers(worker)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Client connected")
        context.add_message(
            {
                "role": "user",
                "content": "Please greet me and offer to check my calendar.",
            }
        )
        await worker.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected")
        await runner.cancel()

    await runner.run()


async def bot(runner_args: RunnerArguments):
    transport = await create_transport(runner_args, transport_params)
    await run_bot(transport, runner_args)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()
