# Implementation plan — Pipecat Cloud × Scalekit

Status: **review only**. No code until you say go. No deploy until you say deploy.

Demo is **Pipecat Cloud only**. No `localhost:7860`. No Whisper. No Kokoro.

## Goal

A reviewer opens a Pipecat Cloud Sandbox URL, clicks Connect, and says “What’s on my calendar today?”

Pipecat Cloud is the voice host (Daily WebRTC is included).
Scalekit AgentKit lists **that user’s** Google Calendar.
The language model never sees an OAuth token.

Same identity contract as the Vapi and LiveKit demos.

## Runtime sequence

1. You open the Cloud dashboard → agent → Sandbox. Click Connect. Speak.
2. Pipecat Cloud (Daily WebRTC) receives audio.
3. Deepgram turns speech into text.
4. The LLM sees text + the tool name `googlecalendar_list_events` only.
5. `bot.py` calls `scalekit_calendar.list_calendar_events` → `execute_tool` as `TEST_IDENTIFIER`.
6. Scalekit uses the stored Google connection. Google returns events.
7. Token fields are stripped. The LLM writes a short spoken answer.
8. Cartesia plays the answer.

Daily room URL and token are created by Pipecat Cloud. We do not sign up for Daily separately.

## Keep (already proven)

| Piece | Why |
| -- | -- |
| `scalekit_calendar.py` | `execute_tool` as `TEST_IDENTIFIER` + `SCALEKIT_CONNECTION_NAME`. Tokens stripped. Unit tests pass. |
| `tests/test_scalekit_calendar.py` | Mocked Scalekit. Keep green. |
| `smoke_calendar.py` | Optional laptop check of Scalekit only. Not the demo. |
| Scalekit Dashboard connection | Google Calendar Active for `TEST_IDENTIFIER`. Already listed events. |

## Change

| File | Change |
| -- | -- |
| `bot.py` | Require Deepgram + Cartesia. Delete Whisper/Kokoro/OpenAI-speech fallback. Keep Daily transport. Drop local `webrtc` as the demo path. |
| `pyproject.toml` | Drop `whisper`, `mlx-whisper`, `kokoro`, `runner` extras. Keep `daily`, `silero`, `deepgram`, `openai`, `cartesia`. |
| `Dockerfile` | **New.** `FROM dailyco/pipecat-base:latest`. Copy `bot.py` + `scalekit_calendar.py`. `uv sync --no-dev`. No `CMD` (base image runs `bot.py`). |
| `pcc-deploy.toml` | **New.** `agent_name = "scalekit-calendar"`. `secret_set = "scalekit-calendar-secrets"`. `[scaling] min_agents = 1`. |
| `.dockerignore` | **New.** Exclude `.env`, `.venv`, tests, markdown, `.agent-status`. |
| `.env.example` | Names only. No values. |
| `README.md` / `RUN.md` | Cloud Sandbox URL. Delete localhost instructions. |

Do not commit `.env`. Do not put secrets in git.

## Secrets (you hold the values)

The agent writes **names**. You put **values** in Pipecat Cloud.

Secret set name: `scalekit-calendar-secrets`

| Name | Who has it |
| -- | -- |
| `SCALEKIT_ENV_URL` | Already in local gitignored `.env` |
| `SCALEKIT_CLIENT_ID` | Same |
| `SCALEKIT_CLIENT_SECRET` | Same |
| `TEST_IDENTIFIER` | Same (`saif.shaik@scalekit.com`) |
| `SCALEKIT_CONNECTION_NAME` | `googlecalendar` |
| `OPENAI_API_KEY` | Scalekit LLM gateway key |
| `OPENAI_BASE_URL` | `https://llm.scalekit.cloud/v1` |
| `OPENAI_MODEL` | `claude-haiku-4-5` |
| `DEEPGRAM_API_KEY` | **You must obtain** |
| `CARTESIA_API_KEY` | **You must obtain** |

You set them in the Cloud dashboard, or you run:

```bash
pipecat cloud secrets set scalekit-calendar-secrets --file .env
```

I do not run that command. I do not read `.env` into chat.

1Password (`op://…` + `op run`) is for a laptop process. Cloud uses the secret set. Same idea: the agent never pastes values.

## You vs me

**You**

1. Create / join a Pipecat Cloud org. [Introduction](https://docs.pipecat.ai/pipecat-cloud/introduction)
2. `uv tool install "pipecat-ai[cli]" --with pipecatcloud`
3. `pipecat cloud auth login` (browser Allow)
4. Get Deepgram + Cartesia keys (or name a different cloud STT/TTS)
5. Paste secret values into the Cloud secret set (or run `secrets set` yourself)
6. After deploy: dashboard → agent `scalekit-calendar` → Sandbox → Allow mic → Connect
7. Say “What’s on my calendar today?”

**Me (after you say go)**

1. Edit `bot.py` and `pyproject.toml` as above
2. Add `Dockerfile`, `pcc-deploy.toml`, `.dockerignore`
3. Keep unit tests green
4. Rewrite `README.md` / `RUN.md` for Cloud
5. Stop. Show you the diff.

**Me (after you say deploy)**

1. `pipecat cloud deploy` from `ecosystem/pipecat-x-sample`
2. Confirm the agent is listed
3. You click Sandbox

## Out of scope

- Local OSS runner as the demo
- Pipecat org GitHub PR
- Email Nina / Slack
- Tutorial agent (later, after Cloud works)
- Extra tools beyond `googlecalendar_list_events`

## Done when

A human (you) hears calendar events from the Cloud Sandbox. SK-1162 stays Todo until that happens. Then we can spawn the tutorial agent.

## Docs

- Deploy: https://docs.pipecat.ai/pipecat-cloud/guides/cloud-builds
- Secrets: https://docs.pipecat.ai/pipecat-cloud/fundamentals/secrets
- Daily WebRTC: https://docs.pipecat.ai/pipecat-cloud/guides/daily-webrtc
- Agent images: https://docs.pipecat.ai/pipecat-cloud/fundamentals/agent-images
