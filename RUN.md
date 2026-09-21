# Run the local Pipecat × Scalekit voice bot

Do this on your machine. Do not start the bot as a background service from an agent.

## One-time setup

```bash
cp .env.example .env
```

Fill `.env` with **your** values. You need:

- `SCALEKIT_ENV_URL`
- `SCALEKIT_CLIENT_ID`
- `SCALEKIT_CLIENT_SECRET`
- `CONNECTED_ACCOUNT_ID` (must match an Active Google Calendar connected account)
- `SCALEKIT_CONNECTION_NAME` (must match the AgentKit connection name, usually `googlecalendar`)
- `OPENAI_API_KEY` (a real OpenAI key)
- `OPENAI_MODEL` (`gpt-4o-mini` unless you set another OpenAI model)
- `DEEPGRAM_API_KEY` — [Deepgram console](https://console.deepgram.com/signup)
- `CARTESIA_API_KEY` — [Cartesia](https://play.cartesia.ai)

Speech keys are required. If they are missing, the bot exits with those signup URLs.

Create your own Google OAuth app and Calendar connection first. See the dashboard steps in [README.md](README.md).

```bash
uv sync
```

## Prove Scalekit (no microphone)

```bash
uv run pytest
```

`smoke_calendar.py` and `roundtrip.py` need live secrets. Run them yourself if you want a live AgentKit check. Do not run them from an unattended agent.

## Start the voice bot

```bash
uv run bot.py
```

Wait until the process prints that the WebRTC server started.

## Open this URL

http://localhost:7860/client

1. Allow the microphone.
2. Click **Connect**.
3. Say: "What's on my calendar today?"

The bot lists **your** calendar. Scalekit `execute_tool` runs as `CONNECTED_ACCOUNT_ID`. The LLM never sees an OAuth token.

Stop the bot with Ctrl+C.

## Scalekit dashboard (only if the calendar tool fails)

1. Open AgentKit → Connections.
2. Confirm Google Calendar is **Active**.
3. Confirm the connected-account identifier equals `CONNECTED_ACCOUNT_ID`.
4. Confirm the connection name equals `SCALEKIT_CONNECTION_NAME`.
