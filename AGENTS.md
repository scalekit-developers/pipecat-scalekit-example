# pipecat-scalekit-example

Starter for other developers. They clone, substitute **their** credentials, and hear **their** Google Calendar.

**Resume:** read [`WIP.md`](WIP.md) first.

Language lives in [`CONTEXT.md`](CONTEXT.md). Decisions live in [`docs/adr/`](docs/adr/). Job notes live on Entire trail 1.

Rules:

- Pipecat OSS on a laptop. Local WebRTC at http://localhost:7860/client.
- Scalekit is AgentKit only (`execute_tool`). Not an LLM product.
- Do not put `llm.scalekit.cloud` in the README.
- Speech is Deepgram + Cartesia. Required. Do not add Whisper or Kokoro.
- Env identifier is `CONNECTED_ACCOUNT_ID`. No `TEST_IDENTIFIER` alias.
- The LLM never sees an OAuth token.
- No Dockerfile. No `pcc-deploy.toml`. No Pipecat Cloud.
- Do not commit `.env`.
- Do not start `bot.py` until a human says **start**.
- Keep Linear mirror in `TRACKER.md`. Keep resume state in `WIP.md`.

## Current block (21 Sep 2026)

`.env` still needs `DEEPGRAM_API_KEY` and `CARTESIA_API_KEY`. Then **start**. Then http://localhost:7860/client.
