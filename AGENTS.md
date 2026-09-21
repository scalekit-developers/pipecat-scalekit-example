# pipecat-sample

Play area for Pipecat × Scalekit.

Tamil's offer (15 Sep, HEY 2092027009): a Pipecat voice agent that uses Scalekit for auth and tool-calling, so it can act in a third-party app on the user's behalf.

Rules:
- Pipecat Cloud only. Do not ship a local OSS runner as the demo.
- Do not email Nina. Do not post Slack.
- Do not open a Pipecat org PR until they ask.
- The LLM never sees an OAuth token. Scalekit `execute_tool` runs as `TEST_IDENTIFIER`.
- Keep state in `TRACKER.md`. It mirrors SK-1162. After a status or next-step change, patch Linear the same way.
