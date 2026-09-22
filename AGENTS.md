# pipecat-scalekit-example

Starter for other developers. They clone, substitute their credentials, and hear their Google Calendar.

Read [README.md](README.md) for setup.

If `notes/WIP.md` exists, read it first. The `notes/` folder is local. It is not part of the starter.

Rules:

- Pipecat OSS on a laptop. Local WebRTC at http://localhost:7860/client.
- Scalekit is AgentKit only (`execute_tool`).
- Do not put `llm.scalekit.cloud` in the README.
- Speech is Deepgram + Cartesia. Required.
- Env identifier is `CONNECTED_ACCOUNT_ID`.
- The LLM never sees an OAuth token.
- No Dockerfile. No `pcc-deploy.toml`. No Pipecat Cloud.
- Do not commit `.env`.
- Do not start `bot.py` until a human says **start**.
