# Pipecat × Scalekit — primary-source research

Language and lock for this sample: [`CONTEXT.md`](CONTEXT.md) and `docs/adr/`. This research predates that lock.

Researched: 2026-09-20. Local proof only. No code changes. No servers started.

Every claim below cites an official URL. If a page is JS-rendered, the same schema is cited from Scalekit’s published connector source that feeds that page.

---

## 1. What Pipecat is in 2026

Pipecat is Daily’s open-source Python framework for real-time voice and multimodal AI agents. It does not own STT, LLM, TTS, or OAuth. It pipelines transport, speech, language, and tools. You pick the providers. BSD-2 license. Python 3.11+. PyPI name: `pipecat-ai`.

Official product line:

> Pipecat is the most widely used open source ecosystem for building voice and multimodal AI agents. Maintained by Daily with the support of the Pipecat developer community.

Pipeline (typical voice turn):

1. Transport receives audio (browser, phone).
2. Speech recognition converts speech to text.
3. LLM generates a response (and may call tools).
4. Speech synthesis converts text to audio.
5. Transport streams audio back.

Round-trip is usually 500–800 ms.

A 2026 bot is also multi-agent-ready: one `PipelineWorker` is a single agent; `WorkerRunner` can coordinate many agents on a bus.

Local run first. Pipecat Cloud is optional production hosting. This demo does not need Cloud.

| Source | URL |
| -- | -- |
| Product | https://www.pipecat.ai/ |
| Docs intro | https://docs.pipecat.ai/pipecat/get-started/introduction |
| GitHub | https://github.com/pipecat-ai/pipecat |
| PyPI | https://pypi.org/project/pipecat-ai/ |

### Version (not 1.11)

`pipecat-ai` **1.11 does not exist**.

| Observation | Value | URL |
| -- | -- | -- |
| GitHub latest release | **v1.8.1** (2026-08-27) | https://github.com/pipecat-ai/pipecat/releases/latest |
| GitHub CHANGELOG on `main` | **[1.8.0] - 2026-08-26**, then 1.8.1 fix | https://github.com/pipecat-ai/pipecat/blob/main/CHANGELOG.md |
| PyPI page title at fetch | v1.6.0 (may lag GitHub) | https://pypi.org/project/pipecat-ai/ |

This sample’s `pyproject.toml` pins `pipecat-ai[...]>=0.0.95`. That lower bound is old. Current constructor style is `settings=Service.Settings(...)` (InputParams deprecated in **v0.0.105**).

https://docs.pipecat.ai/pipecat/fundamentals/service-settings

---

## 2. Function-calling pattern (current)

Preferred pattern: a **direct function**. First argument is always `params: FunctionCallParams`. Tool args follow. Google-style docstring becomes the schema. List the function in `LLMContext(tools=[...])`. Call `await params.result_callback(result)`. Do not give the LLM an OAuth token.

Canonical example: `examples/getting-started/07-function-calling.py`.

https://github.com/pipecat-ai/pipecat/blob/main/examples/getting-started/07-function-calling.py

https://docs.pipecat.ai/pipecat/learn/function-calling

### Direct function

```python
from pipecat.services.llm_service import FunctionCallParams

async def get_current_weather(params: FunctionCallParams, location: str, format: str):
    """Get the current weather.

    Args:
        location: The city and state, e.g. "San Francisco, CA".
        format: The temperature unit to use. Must be either "celsius" or "fahrenheit".
    """
    await params.result_callback({"conditions": "sunny", "temperature": "75"})
```

### Context

```python
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)

context = LLMContext(tools=[get_current_weather, get_restaurant_recommendation])
user_aggregator, assistant_aggregator = LLMContextAggregatorPair(context)
```

System personality is **not** a context message. It is `system_instruction` on the LLM `Settings`.

### FunctionCallParams (docs)

From https://docs.pipecat.ai/pipecat/learn/function-calling and the newer copy at https://docs.pipecat.ai/guides/learn/function-calling:

| Field | Role |
| -- | -- |
| `function_name` | Name the LLM called |
| `tool_call_id` | Unique call id |
| `arguments` | LLM args (use this on classic handlers) |
| `llm` | LLM service |
| `context` | Conversation context |
| `result_callback` | Return the tool result |
| `app_resources` | Optional shared resources |
| `pipeline_worker` | Present on the newer docs page |
| `worker_runner` | Present on the newer docs page |

Direct functions also receive named args after `params`. Classic `FunctionSchema` handlers read `params.arguments`.

### Pipeline (07-function-calling.py)

```
transport.input() → stt → user_aggregator → llm → tts → transport.output() → assistant_aggregator
```

The example uses `PipelineWorker` + `WorkerRunner`, `DeepgramSTTService`, `CartesiaTTSService.Settings(voice=...)`, `OpenAILLMService.Settings(system_instruction=...)`, and `@llm.event_handler("on_function_calls_started")` to speak a filler line.

Verbose alternative: `FunctionSchema(..., handler=...)` listed in `LLMContext(tools=[...])`. Same result path.

---

## 3. How `uv run bot.py` starts the local WebRTC client

The development runner is `pipecat.runner.run.main()`. A bot file must expose `async def bot(runner_args: RunnerArguments)`.

```python
if __name__ == "__main__":
    from pipecat.runner.run import main
    main()
```

```bash
uv add "pipecat-ai[runner]"
uv run bot.py
```

Defaults:

| Item | Value |
| -- | -- |
| Host | `localhost` |
| Port | **7860** |
| Client UI | **http://localhost:7860/client** |
| `GET /` | Redirects to `/client/` |
| Start API | `POST /start` (default transport `"webrtc"`) |
| WebRTC offer | `POST /api/offer` |

Quickstart banner:

```
🚀 WebRTC server starting at http://localhost:7860/client
   Open this URL in your browser to connect!
```

Then click **Connect**.

https://docs.pipecat.ai/pipecat/get-started/quickstart

https://docs.pipecat.ai/pipecat/deployment/running-bots-locally

https://reference-server.pipecat.ai/en/stable/api/pipecat.runner.run.html

### Transport flags

`-t/--transport` restricts the local runner. Omit it to accept all transports. The client may send `transport` in `POST /start`.

| Flag | Meaning |
| -- | -- |
| (none) | All transports. Default `/start` is `webrtc` |
| `-t webrtc` | Local SmallWebRTC + prebuilt UI only |
| `-t daily` | Daily rooms |
| `-t websocket` | Plain WebSocket |
| `-t twilio` / `telnyx` / `plivo` / `exotel` | Telephony |
| `-d` | Direct Daily room (sets daily) |
| `--host` | Default `localhost` |
| `--port` | Default `7860` |
| `-x/--proxy` | Public hostname for telephony webhooks |
| `-v/--verbose` | More logs |

WebRTC path mounts the prebuilt UI at `/client` and bridges `SmallWebRTCConnection` into `bot()`.

The runner is a **local development tool**. It is not Pipecat Cloud. It is not for production.

https://docs.pipecat.ai/pipecat/deployment/running-bots-in-production

---

## 4. STT / TTS options (current Settings constructors)

`InputParams` / `params=` is deprecated as of **v0.0.105**. Use `settings=Service.Settings(...)`. Top-level `model=` / `voice=` still work during deprecation; `settings` wins.

https://docs.pipecat.ai/pipecat/fundamentals/service-settings

### A. Quickstart: Deepgram + Cartesia (cloud)

https://docs.pipecat.ai/pipecat/get-started/quickstart

```python
stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))
tts = CartesiaTTSService(
    api_key=os.getenv("CARTESIA_API_KEY"),
    settings=CartesiaTTSService.Settings(
        voice=os.getenv("CARTESIA_VOICE_ID", "71a7ad14-091c-4e8e-a314-022ece01c121"),
    ),
)
```

Deepgram with explicit settings:

```python
stt = DeepgramSTTService(
    api_key=os.getenv("DEEPGRAM_API_KEY"),
    settings=DeepgramSTTService.Settings(
        model="nova-3",
        language="en",
        smart_format=True,
    ),
)
```

https://docs.pipecat.ai/api-reference/server/services/tts/cartesia

Cartesia extras: `model` default `sonic-3.5` when unset; `generation_config` (volume, speed, emotion); extra `pipecat-ai[cartesia]`. Env: `CARTESIA_API_KEY`.

### B. OpenAI STT + TTS

STT extra: `pipecat-ai[openai]`.

```python
from pipecat.services.openai.stt import OpenAISTTService

stt = OpenAISTTService(
    api_key=os.getenv("OPENAI_API_KEY"),
    settings=OpenAISTTService.Settings(model="gpt-4o-transcribe"),
)
```

Streaming alternative: `OpenAIRealtimeSTTService` (default model `gpt-realtime-whisper`).

https://docs.pipecat.ai/api-reference/server/services/stt/openai

```python
from pipecat.services.openai.tts import OpenAITTSService  # docs also show pipecat.services.openai

tts = OpenAITTSService(
    api_key=os.getenv("OPENAI_API_KEY"),
    settings=OpenAITTSService.Settings(voice="nova"),
)
```

TTS settings: `model`, `voice` (alloy, ash, ballad, cedar, coral, echo, fable, marin, nova, onyx, sage, shimmer, verse), `instructions`, `speed` 0.25–4.0. Output is 24 kHz.

https://docs.pipecat.ai/api-reference/server/services/tts/openai

A Scalekit LLM-gateway key is not an OpenAI speech key. Use Deepgram+Cartesia, real OpenAI speech keys, or local Whisper+Kokoro.

### C. Local Whisper + Kokoro (no speech API keys)

Whisper (CPU/CUDA): `uv add "pipecat-ai[whisper]"`.

```python
from pipecat.services.whisper.stt import WhisperSTTService

stt = WhisperSTTService(settings=WhisperSTTService.Settings(model="base"))
```

Apple Silicon: `uv add "pipecat-ai[mlx-whisper]"`. MLX is macOS arm64 only.

```python
from pipecat.services.whisper.stt import WhisperSTTServiceMLX, MLXModel

stt = WhisperSTTServiceMLX(
    settings=WhisperSTTServiceMLX.Settings(
        model=MLXModel.LARGE_V3_TURBO,
        language=Language.EN,
        temperature=0.0,
    ),
)
```

Defaults: Faster-Whisper `Model.DISTIL_MEDIUM_EN`; MLX `MLXModel.TINY`; `device="auto"`.

https://docs.pipecat.ai/api-reference/server/services/stt/whisper

Kokoro (offline TTS): `pipecat-ai[kokoro]`. No API key. Models download to `~/.cache/pipecat/kokoro-onnx/` on first use.

```python
from pipecat.services.kokoro.tts import KokoroTTSService

tts = KokoroTTSService(settings=KokoroTTSService.Settings(voice="af_heart"))
```

https://docs.pipecat.ai/api-reference/server/services/tts/kokoro

---

## 5. Scalekit AgentKit Python vs Node

**Still correct** for this demo.

### Client

Python SDK constructor is positional:

```python
ScalekitClient(env_url, client_id, client_secret)
```

Source: `sdks/scalekit-sdk-python/scalekit/client.py`.

Docs also show keywords (same three names):

```python
from scalekit import ScalekitClient

scalekit_client = ScalekitClient(
    env_url=os.environ["SCALEKIT_ENV_URL"],  # some pages: SCALEKIT_ENVIRONMENT_URL
    client_id=os.environ["SCALEKIT_CLIENT_ID"],
    client_secret=os.environ["SCALEKIT_CLIENT_SECRET"],
)
actions = scalekit_client.actions
```

https://docs.scalekit.com/agentkit/sdks/python/

https://docs.scalekit.com/agentkit/sdks/python.md

### execute_tool (Python)

Prefer `actions.execute_tool` (runs modifiers). Low-level `tools.execute_tool` uses `params=` instead of `tool_input=` and skips modifiers.

```python
result = actions.execute_tool(
    tool_input={"max_results": 10},
    tool_name="googlecalendar_list_events",
    identifier="user_123",
    connection_name="googlecalendar",
)
# result.data, result.execution_id
```

SDK signature (`scalekit/actions/actions.py`):

```python
def execute_tool(
    self,
    tool_input: ToolInput,
    tool_name: str,
    identifier: Optional[str] = None,
    tool_request: Optional[ToolRequest] = None,
    connected_account_id: Optional[str] = None,
    connection_name: Optional[str] = None,
    **kwargs
) -> ExecuteToolResponse
```

Account resolution: `connected_account_id` **or** (`identifier` + `connection_name`). Not both required together. Output is a wrapper. Read `response.data`.

https://docs.scalekit.com/agentkit/sdks/python/actions/

https://docs.scalekit.com/agentkit/tools/scalekit-optimized-tools/

### executeTool (Node) — same job, different names

```typescript
await scalekit.actions.executeTool({
  toolName: 'googlecalendar_list_events',
  identifier: 'user_123',
  connector: 'googlecalendar',  // Python connection_name
  toolInput: { max_results: 10 },
});
```

https://docs.scalekit.com/agentkit/sdks/node/

https://docs.scalekit.com/agentkit/sdks/node/actions/

| Concept | Python `actions.execute_tool` | Node `actions.executeTool` |
| -- | -- | -- |
| Tool name | `tool_name=` | `toolName` |
| Args | `tool_input=` | `toolInput` |
| User | `identifier=` | `identifier` |
| Connection | `connection_name=` | `connector` (not `connectionName` on execute) |
| Direct account | `connected_account_id=` | `connectedAccountId` |
| Result | `response.data` | `result.data` |

Node `getOrCreateConnectedAccount` uses `connectionName`. Node `executeTool` uses `connector` for that same dashboard Connection name.

The LLM never sees the Google token. Scalekit injects it from the connected account.

For this demo: `identifier=TEST_IDENTIFIER`.

---

## 6. `googlecalendar_list_events` input fields

Tool name is exact: `googlecalendar_list_events`. Do not invent names. Use AgentKit → Connections tool list, or `list_scoped_tools`.

https://docs.scalekit.com/agentkit/tools/agent-tools-quickstart/

https://docs.scalekit.com/agentkit/connectors/googlecalendar/

The public connector HTML table is JS-rendered. The same schema is in Scalekit’s published connector source that feeds that page, and in the auth-stack copies:

`build-with-ai/developer-docs/src/data/agent-connectors/googlecalendar.ts`

Also: https://www.scalekit.com/blog/calendar-scheduling-agent-development (8 Sep 2026): “googlecalendar_list_events documents calendar_id, time_min, time_max, single_events, order_by, and max_results.” Inputs are **snake_case**. CamelCase (`calendarId`, `timeMin`) is a documented demo bug.

Official execute example (minimal):

```python
response = actions.execute_tool(
    tool_name="googlecalendar_list_events",
    identifier="user_123",
    connection_name="googlecalendar",
    tool_input={"max_results": 10},
)
events = response.data.get("events", [])
next_page_token = response.data.get("next_page_token")
```

https://docs.scalekit.com/agentkit/tools/scalekit-optimized-tools/

### Input schema (all optional)

| Field | Type | Required | Meaning |
| -- | -- | -- | -- |
| `calendar_id` | string | no | Calendar to list. Use `"primary"` for the user’s main calendar. |
| `max_results` | integer | no | Max events on this page. |
| `order_by` | string | no | Order of results. Google: `"startTime"` (needs `single_events=true`) or `"updated"`. |
| `time_min` | string | no | Lower bound for event start. RFC3339 (e.g. `2026-09-20T00:00:00Z`). |
| `time_max` | string | no | Upper bound for event start. RFC3339. |
| `single_events` | boolean | no | Expand recurring events into instances. |
| `page_token` | string | no | Next page. |
| `query` | string | no | Free-text search. |
| `schema_version` | string | no | Optional schema version. |
| `tool_version` | string | no | Optional tool version. |

Google Calendar API (provider semantics, not Scalekit-specific): `calendarId=primary`; `orderBy=startTime` only with `singleEvents=true`; `timeMin`/`timeMax` are RFC3339 with a timezone offset.

https://developers.google.com/workspace/calendar/api/v3/reference/events/list

Response keys in Scalekit docs: `events`, `next_page_token` (snake_case). Always read `response.data`.

---

## 7. Dashboard clicks: Scalekit vs Pipecat Cloud

### Local demo: Scalekit Dashboard only

Do **not** open Pipecat Cloud. Local runner is enough.

https://docs.pipecat.ai/pipecat/deployment/running-bots-locally

https://docs.pipecat.ai/pipecat-cloud/introduction

### Scalekit clicks (human)

Site: https://app.scalekit.com

https://docs.scalekit.com/agentkit/quickstart/

https://docs.scalekit.com/agentkit/connections/

https://docs.scalekit.com/agentkit/connected-accounts/

https://docs.scalekit.com/agentkit/tools/authorize/

**A. API credentials (once)**

1. Open the Scalekit Dashboard.
2. Go to **Developers → Settings → API Credentials**.
3. Copy `SCALEKIT_CLIENT_ID`, `SCALEKIT_CLIENT_SECRET`, `SCALEKIT_ENV_URL` (docs also say `SCALEKIT_ENVIRONMENT_URL`).

**B. Connection (once per environment)**

1. Go to **AgentKit → Connections**.
2. If Google Calendar is missing: **Create Connection** / **Add connection** → select **Google Calendar**.
3. Copy the exact **Connection name**. Put it in `SCALEKIT_CONNECTION_NAME`. It is not always the slug `googlecalendar`.
4. Confirm the connection is saved / Active.
5. Optional for a local test: **Use Scalekit credentials**. Use your own Google OAuth client before any public demo.

**C. Connected account (once per identifier)**

1. The per-user record is a **connected account**. It holds the Google tokens. The bot never holds them.
2. Identifier must equal `TEST_IDENTIFIER`.
3. Status must be **ACTIVE** before `execute_tool`.
4. If status is not ACTIVE: open the authorization link (hosted Google consent). Approve Calendar access.
5. Confirm in the Dashboard that that identifier is ACTIVE for that Connection name.

Flow from docs: create connected account → authorization link → user completes OAuth → status `ACTIVE` → execute tools. Scalekit refreshes tokens after that.

Playground (optional check): **AgentKit → Playground**.

https://docs.scalekit.com/agentkit/tools/scalekit-optimized-tools/

### Pipecat Cloud dashboard (do not use for this demo)

Cloud is production hosting. Local `uv run bot.py` does not need an account, deploy, or Cloud API key.

If someone later deploys (not this task):

1. Sign up / `pipecat cloud auth login`.
2. `pipecat cloud secrets set ...` and `pipecat cloud deploy`.
3. Cloud dashboard: select the agent → **Sandbox** → allow microphone → **Connect**.
4. Cloud API keys live under **Settings → API Keys**.

https://docs.pipecat.ai/pipecat/get-started/quickstart (Step 2)

https://docs.pipecat.ai/pipecat-cloud/introduction

### Local bot UI (not a dashboard)

After `uv run bot.py`: open **http://localhost:7860/client** → **Connect**. Speak. That is the runner prebuilt client.

---

## Implications for this local sample

- Keep `FunctionCallParams` + `LLMContext(tools=[googlecalendar_list_events])`.
- Keep `ScalekitClient(env_url, client_id, client_secret)` and `actions.execute_tool(tool_input=..., tool_name=..., identifier=TEST_IDENTIFIER, connection_name=...)`.
- Pass snake_case calendar fields. Default `calendar_id` to `"primary"`. For “today/this week”, pass RFC3339 `time_min` / `time_max`. Set `single_events=True` if `order_by="startTime"`.
- Read `response.data`. Do not parse the wrapper as a list.
- Speech: Deepgram+Cartesia if those keys exist; else OpenAI speech; else local Whisper+Kokoro.
- Do not deploy to Pipecat Cloud. Do not ping Nina. Do not Slack. Do not open a Pipecat org PR.
