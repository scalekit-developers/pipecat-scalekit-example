# Pipecat × Scalekit — Linear mirror

This file stays in sync with [SK-1162](https://linear.app/scalekit/issue/SK-1162/explore-collaboration-opportunities-with-pipecat).

After any session that changes status or next step:
1. Write it here.
2. Patch SK-1162 the same way (description Next + one comment).
3. Resume state lives in `WIP.md`, not here.

**Last synced:** 2026-09-21

Live clone: `/Users/saif/Projects/pipecat-scalekit-example`. Git branch: `prototype`. Entire trail: [trail 1](https://entire.io/gh/saif-shines/pipecat-scalekit-example/trails/1).

## Linear (source of truth for status)

| Field | Value |
| -- | -- |
| Issue | [SK-1162](https://linear.app/scalekit/issue/SK-1162/explore-collaboration-opportunities-with-pipecat) |
| Title | Explore collaboration opportunities with Pipecat |
| Status | Todo |
| Priority | Low |
| Assignee | Saif Ali Shaik |
| Label | DX for growth |

## Next (same text as SK-1162)

Demo is **Pipecat OSS** on the laptop (`http://localhost:7860/client`). Local WebRTC. Deepgram + Cartesia required. Scalekit is AgentKit only (`execute_tool` as `CONNECTED_ACCOUNT_ID`). Real OpenAI key for the LLM. Resume in `WIP.md`. Status stays Todo until a developer hears **their** calendar on localhost.

## Linear comments (newest first)

- **21 Sep** — Grill lock: AgentKit only, `CONNECTED_ACCOUNT_ID`, Deepgram+Cartesia required, real OpenAI key in README. Docs + code on `prototype`. Do not start bot. Do not ping Nina.
- **21 Sep** — Switched demo to Pipecat OSS (local WebRTC). Cloud dropped: no signup credits, PCC-1004. Trail 1 on `prototype`. Do not ping Nina.
- **21 Sep** — Branch `sk-1162-pipecat-cloud-prototype` pushed. Trail create blocked (origin is github-personal, not github.com). Cloud only. Do not ping Nina.
- **20 Sep** — email scan. Tamil emailed Nina 15 Sep. Nina silent. Do not ping.
- **2 Sep** — Tamil will follow up. Low.

## Local only (not a Linear field)

| File | State |
| -- | -- |
| `bot.py` | Pipecat runner + `googlecalendar_list_events`. Deepgram + Cartesia required. Voice server not started by the implementer. |
| `scalekit_calendar.py` | Unit-tested wrapper. `execute_tool` as `CONNECTED_ACCOUNT_ID`. Tokens stripped. |
| `speech_keys.py` | Public helper. Missing keys name Deepgram and Cartesia signups. |
| `pyproject.toml` | No whisper / mlx-whisper / kokoro extras. |
| `.env.example` | Names only. No `OPENAI_BASE_URL`. |
| `tests/` | Calendar seams + speech-key helper. |
| `RUN.md` | Start command and http://localhost:7860/client |
| Run | Developer starts `uv run bot.py`. |

Copy: VAPI / LiveKit identity contract. One tool: `googlecalendar_list_events`.
Python: `client.actions.execute_tool(..., identifier=CONNECTED_ACCOUNT_ID, connection_name=SCALEKIT_CONNECTION_NAME)`.
Pipecat: [07-function-calling.py](https://github.com/pipecat-ai/pipecat/blob/main/examples/getting-started/07-function-calling.py)

## Rules

- Do not email Nina.
- Do not post Slack.
- Do not open a Pipecat org PR until they ask.
- LLM never sees an OAuth token.
- Do not document `llm.scalekit.cloud`.
