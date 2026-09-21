# Pipecat × Scalekit — Linear mirror

This file stays in sync with [SK-1162](https://linear.app/scalekit/issue/SK-1162/explore-collaboration-opportunities-with-pipecat).

After any session that changes status or next step:
1. Write it here.
2. Patch SK-1162 the same way (description Next + one comment).
3. Do not ping Nina.

**Last synced:** 2026-09-21

Git branch: `sk-1162-pipecat-cloud-prototype` (pushed). Entire trail: **not created yet** — `entire trail create` needs a github.com origin and the saif-shines login. Create it in the Entire UI or after we fix origin.

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

Tamil emailed Nina on 15 Sep (HEY 2092027009).
Offer: Saif builds a Pipecat voice-agent sample with Scalekit auth/tool-calling. They only review it. Optional social.

Nina has not replied. Do not ping.

Demo is **Pipecat Cloud only**. Do not use the local OSS runner (`localhost:7860`). Keep Scalekit `execute_tool` as `TEST_IDENTIFIER`. Status stays Todo until someone hears calendar events on a Cloud URL.

## Linear comments (newest first)

- **21 Sep** — Branch `sk-1162-pipecat-cloud-prototype` pushed. Trail create blocked (origin is github-personal, not github.com). Cloud only. Do not ping Nina.
- **20 Sep** — email scan. Tamil emailed Nina 15 Sep. Nina silent. Do not ping.
- **2 Sep** — Tamil will follow up. Low.

## Local only (not a Linear field)

| File | State |
| -- | -- |
| `bot.py` | Pipecat 1.11 runner + `googlecalendar_list_events`. Voice server not started by the implementer. |
| `scalekit_calendar.py` | Unit-tested wrapper. `execute_tool` as `TEST_IDENTIFIER`. Tokens stripped. |
| `pyproject.toml` | `uv sync` done. Pipecat 1.11.0. |
| `.env` | Present (gitignored). |
| `tests/test_scalekit_calendar.py` | 5 unit tests, mocked Scalekit. |
| `RUN.md` | Start command and http://localhost:7860/client |
| Run | User starts `uv run bot.py`. |

Copy: VAPI / LiveKit identity contract. One tool: `googlecalendar_list_events`.
Python: `client.actions.execute_tool(..., identifier=TEST_IDENTIFIER, connection_name=SCALEKIT_CONNECTION_NAME)`.
Pipecat: [07-function-calling.py](https://github.com/pipecat-ai/pipecat/blob/main/examples/getting-started/07-function-calling.py)

## Rules

- Do not email Nina.
- Do not post Slack.
- Do not open a Pipecat org PR until they ask.
- LLM never sees an OAuth token.
