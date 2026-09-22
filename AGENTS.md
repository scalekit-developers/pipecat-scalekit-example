# pipecat-scalekit-example

Starter for other developers. They clone, substitute their credentials, and hear their Google Calendar.

Read [README.md](README.md) for setup.

Rules:

- Pipecat OSS on a laptop. Local WebRTC at http://localhost:7860/client.
- Scalekit is AgentKit only (`execute_tool`).
- Speech is Deepgram + Cartesia. Both are required.
- Env identifier is `CONNECTED_ACCOUNT_ID`.
- The LLM never sees an OAuth token.
- No Dockerfile. No `pcc-deploy.toml`. No Pipecat Cloud.
- Do not commit `.env`.

## Public docs
- README.md is the only human landing page. Keep it under ~80 lines.
- Every claim in README must be followed by the code that proves it.
- Never add roadmap, status tables, or "next up" to README.
- Planning lives in docs/plan/ or the issue tracker. Do not link those from README.
