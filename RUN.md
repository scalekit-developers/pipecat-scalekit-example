# Run the local Pipecat × Scalekit voice bot

Do this on your machine. Do not start the bot as a background service from an agent.

## One-time setup

```bash
cd ecosystem/pipecat-x-sample
cp .env.example .env
```

Fill `.env`. You need:

- `SCALEKIT_ENV_URL` (or `SCALEKIT_ENVIRONMENT_URL`)
- `SCALEKIT_CLIENT_ID`
- `SCALEKIT_CLIENT_SECRET`
- `TEST_IDENTIFIER` (must match an Active Google Calendar connected account)
- `SCALEKIT_CONNECTION_NAME` (must match the AgentKit connection name)
- `OPENAI_API_KEY` (this play area uses the Scalekit LLM gateway)
- `OPENAI_BASE_URL=https://llm.scalekit.cloud/v1`
- `OPENAI_MODEL=claude-haiku-4-5`

Leave `DEEPGRAM_API_KEY` and `CARTESIA_API_KEY` empty unless you have those keys. Empty means local Whisper (MLX) + Kokoro. Do not send the Scalekit LLM gateway key to OpenAI speech.

```bash
uv sync
```

## Prove Scalekit (no microphone)

```bash
uv run python smoke_calendar.py
uv run python roundtrip.py
uv run pytest
```

`smoke_calendar.py` must print `PASS` and exit 0.

## Start the voice bot

```bash
uv run bot.py
```

Wait until the process prints that the WebRTC server started.

The first local-speech run can take about 20 seconds. Whisper and Kokoro download models then. Later runs are faster.

## Open this URL

http://localhost:7860/client

1. Allow the microphone.
2. Click **Connect**.
3. Say: "What's on my calendar today?"

The bot lists **your** calendar. Scalekit `execute_tool` runs as `TEST_IDENTIFIER`. The LLM never sees an OAuth token.

Stop the bot with Ctrl+C.

## Scalekit dashboard (only if smoke fails)

1. Open AgentKit → Connections.
2. Confirm Google Calendar is **Active**.
3. Confirm the connected-account identifier equals `TEST_IDENTIFIER`.
4. Confirm the connection name equals `SCALEKIT_CONNECTION_NAME`.

Do not email Nina. Do not post Slack. Do not open a Pipecat org PR.
