# Pipecat × Scalekit calendar sample

A starter other developers clone. They put their own credentials in `.env` and hear **their** Google Calendar. This trail is Pipecat OSS on a laptop.

## Language

**Developer**:
A person who clones this repository, substitutes their own credentials, and runs the bot.
_Avoid_: reviewer, Nina, Tamil as the person who runs it

**Credential substitution**:
Replacing `.env` values with that developer's AgentKit environment, identifier, OpenAI LLM key, Deepgram key, and Cartesia key. It does not skip Scalekit dashboard setup for Google Calendar.
_Avoid_: "just change the keys" as if no dashboard work exists; Scalekit LLM gateway as a credential to paste

**Identifier**:
The env value Scalekit uses to pick a connected account. The env name is `CONNECTED_ACCOUNT_ID`. Each developer sets it to **their** connected-account identifier.
_Avoid_: TEST_IDENTIFIER, user id, account id as the env name

**Pipecat OSS**:
The Python library `pipecat-ai` running on this laptop, with local WebRTC.
_Avoid_: Cloud, Sandbox, "the Pipecat product" as if it were one runtime

**Pipecat Cloud**:
Daily's hosted agent runtime. Out of scope for this trail.
_Avoid_: calling the laptop demo Cloud

**Connection**:
A Scalekit AgentKit connector configuration. This sample uses the name `googlecalendar`.
_Avoid_: connected account, credential, integration

**Connected account**:
One person's authorized Google Calendar, stored by Scalekit and keyed by an identifier.
_Avoid_: connection, user, credential

**AgentKit**:
The Scalekit product this sample shows. Connected accounts, `execute_tool`, Google Calendar. Not an LLM product.
_Avoid_: llm.scalekit.cloud, Scalekit LLM gateway

**LLM**:
A chat model. Required. Separate from AgentKit. Developers use a real OpenAI key, like the Pipecat quickstart.
_Avoid_: treating Scalekit as the LLM product

**Internal LLM proxy**:
`llm.scalekit.cloud`. A Scalekit-team-only proxy for demo apps. Not a product. Not in the README. Team members may use it or a real OpenAI key for their own run.
_Avoid_: Scalekit LLM product, documenting it for external developers

**execute_tool**:
The AgentKit call that runs a named tool as an identifier. The language model never sees a Google token.
_Avoid_: connector, MCP, "the Scalekit SDK" as the tool itself

**Google OAuth app**:
The developer’s own Google Cloud OAuth client, registered on the Scalekit Google Calendar connection. Required for this sample.
_Avoid_: Scalekit-managed OAuth app as something this sample waits for

**Scalekit-managed OAuth app**:
Scalekit's shared OAuth client for a provider. Not available for Google Calendar in this sample. A future Scalekit feature may add it. This sample does not wait.
_Avoid_: managed credentials as a name for the user's Google token

**User token vault**:
Scalekit-stored Google access and refresh tokens for a connected account.
_Avoid_: Scalekit-managed OAuth app, API key

**Trail**:
One Entire job. This sample is trail 1 on git branch `prototype`.
_Avoid_: git branch, Linear ticket, checkpoint

**Git branch**:
`prototype`. Git owns the commits. The trail owns the job notes.
_Avoid_: trail

**Speech**:
Deepgram for hearing. Cartesia for speaking. Required in this sample. Matches the Pipecat quickstart. The README points developers to those signups. This sample does not add Whisper or Kokoro as extra products.
_Avoid_: Whisper, Kokoro, local models as a second path

**Local WebRTC**:
The laptop audio path. Browser at http://localhost:7860/client. No Daily key. No Pipecat Cloud.
_Avoid_: Daily rooms, Sandbox, Cloud transport
