# Implementation plan — Pipecat OSS × Scalekit

Status: **locked**. Code and docs match CONTEXT.md. Do not start `bot.py` until a human says start.

Demo is **Pipecat OSS on this laptop**. No Pipecat Cloud. No Cloud card. No Dockerfile.

## Goal

A developer clones this repo, substitutes **their** credentials, opens http://localhost:7860/client, and hears **their** Google Calendar.

Pipecat OSS is the voice host (local WebRTC).
Scalekit AgentKit lists that developer's Google Calendar.
The language model never sees an OAuth token.

## Runtime sequence

1. Developer runs `uv run bot.py`. Opens http://localhost:7860/client. Clicks Connect. Speaks.
2. Local WebRTC receives audio. No Daily key. No Cloud session.
3. Deepgram turns speech into text.
4. The LLM sees text + the tool name `googlecalendar_list_events` only.
5. `bot.py` calls `scalekit_calendar.list_calendar_events` → `execute_tool` as `CONNECTED_ACCOUNT_ID`.
6. Scalekit uses the stored Google connection. Google returns events.
7. Token fields are stripped. The LLM writes a short spoken answer.
8. Cartesia plays the answer.

## Keep

| Piece | Why |
| -- | -- |
| `bot.py` | Local runner + WebRTC. Deepgram + Cartesia required. |
| `scalekit_calendar.py` | `execute_tool` as `CONNECTED_ACCOUNT_ID` + `SCALEKIT_CONNECTION_NAME`. Tokens stripped. |
| `speech_keys.py` | Fails with Deepgram and Cartesia signup URLs if keys are missing. |
| `tests/test_scalekit_calendar.py` | Mocked Scalekit. Identifier env is `CONNECTED_ACCOUNT_ID`. |
| `tests/test_speech_keys.py` | Speech-key helper. |
| `smoke_calendar.py` | Laptop check of Scalekit only. No microphone. |
| `pyproject.toml` | `runner`, `webrtc`, `silero`, `deepgram`, `openai`, `cartesia`. No Whisper or Kokoro. |
| `RUN.md` | Local start + http://localhost:7860/client |

Do not add `Dockerfile` or `pcc-deploy.toml`. Do not commit `.env`.

## Env (names only)

| Name | Role |
| -- | -- |
| `SCALEKIT_ENV_URL` | AgentKit environment |
| `SCALEKIT_CLIENT_ID` | Client id |
| `SCALEKIT_CLIENT_SECRET` | Client secret |
| `CONNECTED_ACCOUNT_ID` | Developer's connected-account identifier |
| `SCALEKIT_CONNECTION_NAME` | `googlecalendar` |
| `OPENAI_API_KEY` | Real OpenAI key |
| `OPENAI_MODEL` | `gpt-4o-mini` |
| `DEEPGRAM_API_KEY` | Required |
| `CARTESIA_API_KEY` | Required |

Do not document `OPENAI_BASE_URL`. Code may still honor it if set.

## Out of scope

- Pipecat Cloud deploy, card, Sandbox
- Whisper / Kokoro as a second speech path
- Documenting `llm.scalekit.cloud`
- Pipecat org GitHub PR
- Email Nina / Slack
- Extra tools beyond `googlecalendar_list_events`
- Moving the repo to `scalekit-developers`

## Done when

A developer hears **their** calendar events at http://localhost:7860/client.

## Docs

- Local runner: https://docs.pipecat.ai/pipecat/deployment/running-bots-locally
- Quickstart: https://docs.pipecat.ai/pipecat/get-started/quickstart
- Function calling: https://docs.pipecat.ai/guides/learn/function-calling
- Scalekit tools: https://docs.scalekit.com/agentkit/tools/scalekit-optimized-tools
- Google Calendar connector: https://docs.scalekit.com/agentkit/connectors/googlecalendar/
- Connections: https://docs.scalekit.com/agentkit/connections
