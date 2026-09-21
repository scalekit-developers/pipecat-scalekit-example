# Pipecat Cloud credits (signup)

Researched: 2026-09-21. Official pages only. No code. No ping.

## 1. Free credits on first signup?

**No prepaid dollar credits.** Official docs do not say a new account gets a credit wallet, trial balance, or signup coupon.

Pipecat Cloud is **usage-based**. You pay for minutes. You must have a **billing account** before you start a session.

> You must have an active billing account to start sessions. Usage is billed for the duration of each session.

https://docs.pipecat.ai/pipecat-cloud/fundamentals/active-sessions

> Pipecat Cloud uses usage-based pricing.

https://docs.pipecat.ai/pipecat-cloud/introduction

> In order to deploy or start an agent on Pipecat Cloud, you must have valid billing credentials set up on the namespace or organization you have specified. You can set up these up via the Pipecat Cloud dashboard.

Error **PCC-1004**: “Billing credentials not set.”

https://docs.pipecat.ai/pipecat-cloud/fundamentals/error-codes

Signup page (https://pipecat.daily.co/sign-up) does not mention credits.

Do not mix this with Daily Video SDK credits from 2022 ($15 after card, 10k free minutes). That post is not Pipecat Cloud.

https://www.daily.co/blog/announcing-our-new-pricing/

## 2. What *is* free, and when it appears

These are **included rates**, not a dashboard credit line.

| Item | What official copy says | When |
| -- | -- | -- |
| Daily WebRTC voice, 1:1, on the Cloud-provisioned Daily key | “Free voice minutes” for one human + one agent. Pricing table: Daily WebRTC Voice **$0.001 Free** for 1:1 on Pipecat Cloud. | After signup. A Daily API key is provisioned automatically. |
| Krisp VIVA | First 10,000 active session minutes / month **Free**. Then $0.0015/min. | After you enable Krisp on a Cloud deploy. |
| Auto-scale buffer | Extra idle agents during spikes: **no additional cost**. | During traffic. |
| Agent hosting | **Not free.** agent-1x **$0.01/min** active, **$0.0005/min** reserved. | When a session runs, or when `min-agents` ≥ 1. |

https://docs.pipecat.ai/pipecat-cloud/guides/daily-webrtc

https://www.daily.co/pricing/pipecat-cloud/

https://docs.pipecat.ai/pipecat-cloud/guides/krisp-viva

https://docs.pipecat.ai/pipecat-cloud/fundamentals/scaling

No official page says credits appear after email verify, first deploy, or adding a card.

## 3. Why the dashboard can show $0 / no credits

1. **There is no credit balance.** Billing is pay-as-you-go. $0 usage is normal before a session.
2. **No billing credentials yet.** Deploy/start needs a card on the org. PCC-1004.
3. **Wrong workspace.** Billing is **organization-level**, not always the personal workspace.
   https://docs.pipecat.ai/pipecat-cloud/fundamentals/accounts-and-organizations
4. **Looking at “credits” instead of usage.** Included 1:1 voice minutes do not show as dollars.
5. **Agent hosting still bills** even when transport is free. A Sandbox session costs agent minutes.

## 4. What to click (two steps)

1. Open the Pipecat Cloud dashboard → **Settings → Billing**.
2. Add **billing credentials** (payment method). Optional: set a **spend limit** on the same page (`pipecat cloud spend-limit set …` also works).

https://docs.pipecat.ai/pipecat-cloud/fundamentals/scaling

https://docs.pipecat.ai/pipecat-cloud/fundamentals/error-codes

Then you can deploy. Hosting still bills per minute. LLM/STT/TTS keys are separate (Deepgram, OpenAI, Cartesia).

Support if billing is stuck: help@daily.co
