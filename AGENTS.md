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
