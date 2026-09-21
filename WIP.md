# WIP — resume this trail

Read this first in a new session. Then `AGENTS.md` and `CONTEXT.md`.

## Where

| Item | Value |
| -- | -- |
| Clone | `/Users/saif/Projects/pipecat-scalekit-example` |
| GitHub | `saif-shines/pipecat-scalekit-example` (private) |
| Branch | `prototype` |
| Trail | https://entire.io/gh/saif-shines/pipecat-scalekit-example/trails/1 |
| Entire CLI | `--context in.auth.entire.io` (saif-shines) |
| Linear | SK-1162 Todo |
| Tip | `89f50d5` on 21 Sep 2026 |

Git owns commits. The trail owns the job notes.

## Locked decisions

- Starter for **other developers**. They substitute **their** creds and hear **their** calendar.
- Pipecat **OSS**. Local WebRTC. http://localhost:7860/client
- Scalekit = **AgentKit only** (`execute_tool`). Not an LLM product.
- `llm.scalekit.cloud` is an internal team proxy. Not a product. Not in the README.
- LLM in README = real OpenAI key. Team members may use the internal proxy in their own `.env`.
- Speech = Deepgram + Cartesia. Required. README links to signups. No Whisper. No Kokoro.
- Identifier env = `CONNECTED_ACCOUNT_ID`. No `TEST_IDENTIFIER` alias.
- Google OAuth app = developer creates their own. Scalekit-managed creds later, not this sample.
- No Dockerfile. No `pcc-deploy.toml`. No Pipecat Cloud.
- Repo stays private this trail. Do not move to `scalekit-developers` here.

Language: `CONTEXT.md`. ADRs: `docs/adr/0001`–`0005`.

## Done

- Grill confirmed.
- Implement with Matt `/implement` + `/tdd`. Commit `3a2b9b9`.
- Matt `/code-review` vs `ec2e063...HEAD`: 0 hard findings.
- ADR 0005 stale sentence fixed in `89f50d5`.
- `uv run pytest`: 10 passed.
- `uv run python smoke_calendar.py`: PASS. 5 events. No token to the LLM.

## Blocked

`.env` has AgentKit + LLM. **`DEEPGRAM_API_KEY` and `CARTESIA_API_KEY` are empty.**

`uv run bot.py` will fail until those two are set.

New Deepgram account: $200 free credit, no card. https://deepgram.com/pricing  
New Cartesia free plan: 20K credits / month. https://www.cartesia.ai/pricing  

That is not Pipecat Cloud billing.

## Resume

1. `cd /Users/saif/Projects/pipecat-scalekit-example && git checkout prototype && git pull`
2. Paste Deepgram and Cartesia keys into `.env` (do not commit `.env`).
3. Human says **start**.
4. Agent runs `uv run bot.py`.
5. Human opens http://localhost:7860/client, clicks Connect, hears calendar.

Trail is done when a human hears calendar events on localhost.

## Roles (keep)

- Parent talks to the human. Entire trail 1 stays the one job.
- Researcher: Exa, official docs, only if a fact is open.
- Implementer: Matt `/implement` + `/tdd`.
- Reviewer: Matt `/code-review` (Standards + Spec).
- Do not start `bot.py` until the human says **start**.
