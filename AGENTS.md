# pipecat-scalekit-example

Starter for other developers. They clone, substitute **their** credentials, and hear **their** Google Calendar.

Language lives in [`CONTEXT.md`](CONTEXT.md). Decisions live in [`docs/adr/`](docs/adr/).

Rules:

- Pipecat OSS on a laptop. Local WebRTC at http://localhost:7860/client.
- Scalekit is AgentKit only (`execute_tool`). Not an LLM product.
- Do not put `llm.scalekit.cloud` in the README.
- Speech is Deepgram + Cartesia. Required. Do not add Whisper or Kokoro.
- Env identifier is `CONNECTED_ACCOUNT_ID`. No `TEST_IDENTIFIER` alias.
- The LLM never sees an OAuth token.
- No Dockerfile. No `pcc-deploy.toml`. No Pipecat Cloud.
- Do not commit `.env`.
- Keep state in `TRACKER.md`.
