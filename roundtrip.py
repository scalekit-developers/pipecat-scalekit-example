"""Text round-trip: LLM -> Scalekit calendar tool -> spoken-style answer.

No microphone. Proves the same identity contract the Pipecat bot uses.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv
from scalekit import ScalekitClient

load_dotenv(Path(__file__).with_name(".env"))


def _env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def _execute_calendar() -> dict:
    env_url = _env("SCALEKIT_ENV_URL", "SCALEKIT_ENVIRONMENT_URL")
    client = ScalekitClient(
        env_url, _env("SCALEKIT_CLIENT_ID"), _env("SCALEKIT_CLIENT_SECRET")
    )
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    response = client.actions.execute_tool(
        tool_input={
            "calendar_id": "primary",
            "max_results": 5,
            "single_events": True,
            "order_by": "startTime",
            "time_min": start.isoformat().replace("+00:00", "Z"),
            "time_max": end.isoformat().replace("+00:00", "Z"),
        },
        tool_name="googlecalendar_list_events",
        identifier=_env("TEST_IDENTIFIER"),
        connection_name=_env("SCALEKIT_CONNECTION_NAME") or "googlecalendar",
    )
    data = response.data if hasattr(response, "data") else response
    return data if isinstance(data, dict) else {"data": data}


def _chat(messages: list[dict], tools: list[dict] | None = None) -> dict:
    key = _env("OPENAI_API_KEY")
    base = (_env("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = _env("OPENAI_MODEL") or "claude-haiku-4-5"
    body: dict = {"model": model, "messages": messages, "max_tokens": 400}
    if tools:
        body["tools"] = tools
        body["tool_choice"] = "auto"
    r = httpx.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    if r.status_code >= 400:
        print("LLM_HTTP", r.status_code, r.text[:1200], file=sys.stderr)
        r.raise_for_status()
    return r.json()["choices"][0]["message"]


def main() -> int:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "googlecalendar_list_events",
                "description": "List the user's Google Calendar events. Default calendar_id is primary.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {"type": "string"},
                        "time_min": {"type": "string"},
                        "time_max": {"type": "string"},
                    },
                },
            },
        }
    ]
    messages = [
        {
            "role": "system",
            "content": "You are a voice assistant. Use googlecalendar_list_events. Default calendar_id to primary. Keep the answer short and spoken.",
        },
        {"role": "user", "content": "What's on my calendar today?"},
    ]
    first = _chat(messages, tools)
    tool_calls = first.get("tool_calls") or []
    if not tool_calls:
        print("FAIL LLM did not call googlecalendar_list_events")
        print(json.dumps(first, default=str)[:800])
        return 1

    name = tool_calls[0]["function"]["name"]
    if name != "googlecalendar_list_events":
        print("FAIL unexpected tool", name)
        return 1

    result = _execute_calendar()
    events = result.get("events") or result.get("items") or []
    messages.append(first)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_calls[0]["id"],
            "content": json.dumps(result, default=str)[:6000],
        }
    )
    answer = _chat(messages, tools)
    spoken = (answer.get("content") or "").strip()
    if not spoken:
        print("FAIL empty spoken answer")
        return 1
    print("PASS roundtrip")
    print("tool", name)
    print("event_count", len(events) if isinstance(events, list) else 0)
    print("answer", spoken)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("FAIL", exc, file=sys.stderr)
        raise SystemExit(1)
