# Pipecat × Scalekit calendar sample

> A Pipecat voice bot that reads your Google Calendar through Scalekit AgentKit.

Watch the demo: https://screen.studio/share/86SdvaHM

This sample is [Pipecat OSS](https://docs.pipecat.ai/pipecat/get-started/quickstart) on a laptop. Scalekit is **AgentKit only**: a connection, a connected account, and `execute_tool`. Scalekit is not the language model.

```
Developer (browser at http://localhost:7860/client)
   │  local WebRTC audio
   ▼
Pipecat bot.py  (this process)
   │  googlecalendar_list_events
   ▼
Scalekit AgentKit execute_tool(CONNECTED_ACCOUNT_ID)
   │
   ▼
Google Calendar (your connected account)
```

- The browser never sees a Scalekit secret.
- The LLM never sees an OAuth token.
- `execute_tool` runs as `CONNECTED_ACCOUNT_ID`.

## Quickstart

One-time setup (accounts + dashboard config) is below. Once `.env` is filled:

```bash
uv sync
uv run bot.py
```

Open http://localhost:7860/client. Allow the microphone. Click **Connect**. Say "What's on my calendar today?" — the bot lists **your** calendar.

## You need

- Python 3.11+ and [uv](https://docs.astral.sh/uv/)
- A [Scalekit](https://scalekit.com) environment (AgentKit)
- A [Google Cloud](https://console.cloud.google.com/apis/credentials) OAuth client
- A real [OpenAI](https://platform.openai.com/api-keys) API key (same as the Pipecat quickstart)
- [Deepgram](https://console.deepgram.com/signup) and [Cartesia](https://play.cartesia.ai) keys (same as the Pipecat quickstart)

## Scalekit dashboard (Google Calendar)

Google Calendar has no Scalekit-managed OAuth app in this sample. Create your own Google OAuth app, then paste it into Scalekit.

1. In the Scalekit Dashboard go to **AgentKit → Connections → Add connection**. Choose **Google Calendar**. Set the connection name to `googlecalendar`.
2. Copy the Scalekit **Redirect URI**.
3. In [Google Cloud Console](https://console.cloud.google.com/apis/credentials) create an OAuth client (Web application). Add that Redirect URI. Enable the Google Calendar API.
4. Paste the Google **Client ID** and **Client Secret** into the Scalekit connection. Save.
5. In **AgentKit → Connected Accounts**, connect **your** Google account. Use an identifier you will put in `.env` as `CONNECTED_ACCOUNT_ID`. Confirm the connected account is **Active**.

Copy `SCALEKIT_ENV_URL`, `SCALEKIT_CLIENT_ID`, and `SCALEKIT_CLIENT_SECRET` from the Scalekit Dashboard into `.env`.

See [Configure a connection](https://docs.scalekit.com/agentkit/connections) and [Google Calendar connector](https://docs.scalekit.com/agentkit/connectors/googlecalendar/).

## Setup

```bash
cp .env.example .env
# fill .env with your values
uv sync
uv run pytest
```

Then run the Quickstart commands above. If speech keys are missing, the process exits with an error that includes the Deepgram and Cartesia signup URLs.

## Env names

| Name | Role |
| -- | -- |
| `SCALEKIT_ENV_URL` | AgentKit environment URL |
| `SCALEKIT_CLIENT_ID` | Scalekit client id |
| `SCALEKIT_CLIENT_SECRET` | Scalekit client secret |
| `CONNECTED_ACCOUNT_ID` | **Your** connected-account identifier |
| `SCALEKIT_CONNECTION_NAME` | `googlecalendar` |
| `OPENAI_API_KEY` | Real OpenAI key |
| `OPENAI_MODEL` | `gpt-4o-mini` (or another OpenAI model) |
| `DEEPGRAM_API_KEY` | Required |
| `CARTESIA_API_KEY` | Required |

Do not commit `.env`.

## What this is not

- Not Pipecat Cloud. No Dockerfile. No `pcc-deploy.toml`.
- Not a Scalekit LLM product. The LLM is OpenAI.
- Not Whisper or Kokoro. Speech is Deepgram + Cartesia.

## Docs

- [Pipecat local runner](https://docs.pipecat.ai/pipecat/deployment/running-bots-locally)
- [Pipecat quickstart](https://docs.pipecat.ai/pipecat/get-started/quickstart)
- [Scalekit execute_tool](https://docs.scalekit.com/agentkit/tools/scalekit-optimized-tools)
