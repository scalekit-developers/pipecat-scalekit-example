# Pipecat × Scalekit (local play area)

A Pipecat voice agent that lists **Google Calendar** through **Scalekit AgentKit**.

Tamil's 15 Sep offer: a working Pipecat example that uses Scalekit for auth and tool-calling, so the agent can act in a third-party app on the user's behalf. Nina only reviews. Optional social later.

This folder is local proof. Do not email Nina. Do not open a Pipecat org PR until they ask.

Same identity contract as [vapi-scalekit-voice-demo](../vapi-scalekit-voice-demo) and [livekit-scalekit-voice-demo](../livekit-scalekit-voice-demo):

- The browser never sees a Scalekit secret.
- The LLM never sees an OAuth token.
- `execute_tool` runs as `TEST_IDENTIFIER`.

```
User (browser at :7860/client)
   │  WebRTC audio
   ▼
Pipecat bot.py  (this process)
   │  googlecalendar_list_events
   ▼
Scalekit AgentKit execute_tool(identifier)
   │
   ▼
Google Calendar (user's connected account)
```

Pipecat is Python. Vapi and LiveKit demos are Node. The Scalekit call is the same idea.

## Run

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/).

Required keys: Scalekit AgentKit plus an OpenAI-compatible LLM key (`OPENAI_API_KEY`). This play area uses Scalekit's LLM gateway. Deepgram and Cartesia are optional. Without them the bot uses local Whisper and Kokoro for speech.

```bash
cd ecosystem/pipecat-x-sample
cp .env.example .env
# fill .env
uv sync
uv run bot.py
```

Open http://localhost:7860/client. Click Connect. Say:

- "What's on my calendar today?"
- "Do I have meetings this week?"

## Scalekit dashboard

1. AgentKit → Connections → Google Calendar is Active.
2. The connected-account **identifier** matches `TEST_IDENTIFIER`.
3. The connection **name** matches `SCALEKIT_CONNECTION_NAME`.

## What this is not

- Not published to GitHub yet.
- Not a Pipecat Cloud deploy.
- Not a docs or cookbook PR.
- Not a ping to Nina.

Ticket: [SK-1162](https://linear.app/scalekit/issue/SK-1162/explore-collaboration-opportunities-with-pipecat).
