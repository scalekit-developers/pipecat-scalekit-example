# Secrets for coding agents

Researched: 2026-09-20. No code. No keys in this file.

**Goal:** the agent writes `os.getenv("NAME")`. The human puts the value somewhere the agent never reads. The process that runs the bot sees the value. The chat does not.

---

## Rule

| Who | Does | Does not |
| -- | -- | -- |
| Human | Stores the value in a vault, dashboard, or a gitignored local env | Pastes the value into chat |
| Agent | Writes code that reads **names** | Opens `.env`, `mcp.json` env blocks, shell profiles, or vault dumps |
| Runtime | Injects values into the child process | Logs them |

1Password’s own AI-access page: paste a secret into an agent and it can leak into LLM context. Same for plaintext `.env` and `mcp.json`.

https://www.1password.dev/get-started/secure-ai-access

---

## 1. Secret managers the agent can *start*, not *read*

These CLIs load values into a **subprocess**. The command the agent writes is a **name**. The human authenticates the CLI once (desktop app, Touch ID, or a service token the human sets outside chat).

### 1Password CLI + Environments (best fit for a laptop agent)

- `.env` holds `op://vault/item/field` **references**, not values. Or a 1Password Environment ID.
- `op run -- uv run bot.py` injects values only for that process.
- Stdout/stderr that reprint a secret are **masked by default**. `--no-masking` prints them. Do not use that with an agent watching the terminal.
- Service accounts: `OP_SERVICE_ACCOUNT_TOKEN`, scoped to one vault. Least privilege.
- MCP wrapper: `"command": "op", "args": ["run", "--environment", "<id>", "--", "npx", ...]` so `mcp.json` has **no** tokens.

https://www.1password.dev/cli/secrets-environment-variables

https://www.1password.dev/cli/reference/commands/run

https://www.1password.dev/service-accounts/use-with-1password-cli

**1Password MCP (2026):** the agent may **list variable names** and manage Environments. Official line: the MCP server **does not return secret values** to the client. Every write needs a 1Password approval prompt. Mounted `.env` is not stored on disk and is not in Git (Mac/Linux).

https://www.1password.dev/environments/mcp-server

https://www.1password.dev/get-started/secure-ai-access

### Infisical

```bash
infisical run --env=dev -- uv run bot.py
```

Human logs in once (`infisical login`) or sets `INFISICAL_TOKEN` outside the agent. Prefer this over writing a `.env`. `infisical secrets generate-example-env` writes **names** (and optional `DEFAULT:` comments), not live values.

https://infisical.com/docs/cli/commands/run

https://infisical.com/docs/documentation/platform/secrets-mgmt/concepts/secrets-delivery

### Doppler

```bash
doppler run -- uv run bot.py
```

Human: `doppler login` locally, or `DOPPLER_TOKEN` / service token in CI. Doppler warns that some env names can change process behavior; they prefer ephemeral files for the highest-risk cases. For this demo, `doppler run` is enough.

https://docs.doppler.com/docs/cli

https://docs.doppler.com/docs/accessing-secrets

https://docs.doppler.com/docs/service-tokens

### HashiCorp Vault Agent (process supervisor)

Vault Agent renders `env_template` blocks, then `exec`s the app. The app only sees env vars. The agent in chat never talks to Vault.

https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent/process-supervisor

https://developer.hashicorp.com/vault/tutorials/vault-agent/agent-env-vars

### Cloud stores (runtime, not chat)

The **deployed** process fetches by **name/ARN**. The coding agent commits the name only. IAM/OIDC is the auth, not a pasted key.

- AWS Secrets Manager `GetSecretValue` — https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
- GCP Secret Manager → Cloud Run env or volume — https://docs.cloud.google.com/run/docs/configuring/services/secrets
- Same idea on Azure Key Vault.

GitHub Actions can use **OIDC** to the cloud so the workflow stores **no** long-lived cloud key.

https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets

---

## 2. Hosted secret *sets* (agent deploys a name)

Human (or a one-shot CLI the human runs) puts the **value** in the platform. The agent’s files mention only the **set name** or `${{ secrets.NAME }}`.

### Pipecat Cloud

```bash
# human, once — do not paste the values into chat
pipecat cloud secrets set my-secrets --file .env
```

Agent writes `secret_set = "my-secrets"` in `pcc-deploy.toml` and `os.getenv("SCALEKIT_CLIENT_SECRET")` in code. Secrets mount as env. `GET /secrets/{setName}` returns **key names, not values**. This local demo does **not** need Cloud.

https://docs.pipecat.ai/pipecat-cloud/fundamentals/secrets

https://docs.pipecat.ai/api-reference/pipecat-cloud/rest-reference/endpoint/secret-list-one

### GitHub Actions

Human: repo **Settings → Secrets and variables → Actions**. Agent YAML:

```yaml
env:
  SCALEKIT_CLIENT_SECRET: ${{ secrets.SCALEKIT_CLIENT_SECRET }}
```

GitHub redacts known secrets in logs. Do not `echo` them. Do not pass them on the command line (`ps` can see argv). Prefer env / STDIN.

https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets

https://docs.github.com/en/actions/concepts/security/secrets

### GitHub Copilot cloud agent (2026)

Dedicated **Agents** secrets (not Actions secrets). Human: **Settings → Secrets and variables → Agents**. Values become env in the agent VM. Session logs **mask** secret values. MCP-only secrets use the `COPILOT_MCP_` prefix. Org-level sharing shipped 8 May 2026.

https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables

https://github.blog/changelog/2026-05-08-more-flexible-secrets-and-variables-for-copilot-cloud-agent/

### Vercel

Human: project **Environment Variables**, type **Secret** (write-only after save). Agent never needs the value. Redeploy to pick up a rotation. `vercel env pull` for Development Secrets may write a **placeholder**, not the real value — keep local secrets out of Git.

https://vercel.com/docs/environment-variables

https://vercel.com/docs/environment-variables/sensitive-environment-variables

---

## 3. Safe local pattern (this sample)

1. Agent writes Python that only calls `os.getenv("SCALEKIT_CLIENT_SECRET")` (and the other **names**).
2. Agent commits `.env.example` with **empty** keys / comments. Infisical can generate that file from names.
3. Human gitignores `.env`. Human fills `.env` **in the terminal or a password manager**, not in chat.
4. Better: no plaintext `.env`. Human runs `op run -- uv run bot.py` (or Infisical/Doppler).
5. Agent must not log `os.environ`, `printenv`, or the Scalekit client object.
6. Claude Code: deny reading env files.

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  }
}
```

https://code.claude.com/docs/en/settings

Claude Code can also set `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` so child shells do not inherit Anthropic/cloud credentials (cuts prompt-injection theft via `echo $KEY`).

https://code.claude.com/docs/en/env-vars.md

7. 1Password hook (Cursor plugin / Claude / Copilot / Windsurf): fail the agent’s shell if the mounted Environment `.env` is missing. The agent is told to fix setup, not given the value.

https://www.1password.dev/get-started/secure-ai-access

---

## 4. Patterns that still leak

| Leak | Why |
| -- | -- |
| Paste key in chat | Lands in LLM context, provider logs, session memory. 1Password: do not do this. |
| Commit `.env` | Git history keeps it forever. GitHub push protection may block known token shapes, but not every key. |
| Agent `Read(.env)` | Same as pasting. Deny the tool. |
| `printenv`, debug logs, exception dumps | GitHub says redaction is **not guaranteed**. Pipecat/Vercel also redact only when they recognize the value. |
| Screenshot of API Credentials | Image → OCR → context. Copy names only. |
| `mcp.json` `env: { "TOKEN": "sk-..." }` | Agent-readable JSON. Wrap with `op run`. |
| Shell profile `export KEY=sk-...` | Agent can `cat ~/.zshrc`. Use 1Password shell plugins or `op run`. |
| `op run --no-masking` / `op inject` to a file the agent can read | Defeats masking. Delete injected files. |
| Moving a plaintext `.env` into 1Password **without rotating** | Official 1Password note: past Git history and **agent memory** still hold the old value. Rotate. |

https://docs.github.com/en/code-security/concepts/secret-security/push-protection

https://docs.github.com/en/code-security/how-tos/use-ghas-with-ai-coding-agents/scan-for-secrets-with-github-mcp-server

---

## 5. What is new in 2025–2026 for *agent* credentials

| Thing | What it is | Official? |
| -- | -- | -- |
| **1Password Environments + MCP** | Agent manages **names**. Values never returned. Approval prompt per write. `op run --environment` for MCP. Mounted `.env` not on disk. | Yes — https://www.1password.dev/environments/mcp-server |
| **1Password “Secure AI access”** | Stated policy: nothing in plaintext, `mcp.json`, or LLM context. Hooks + Cursor plugin. | Yes — https://www.1password.dev/get-started/secure-ai-access |
| **GitHub Copilot Agents secrets** | Secret set for the cloud coding agent. Masked logs. Org-wide. `COPILOT_MCP_*` for MCP only. (May 2026) | Yes — GitHub Docs + Changelog |
| **GitHub MCP secret scanning** | Agent can scan diffs for leaked keys **before** commit. Push protection also blocks GitHub MCP on public repos. Findings are session-only. | Yes — https://docs.github.com/en/code-security/how-tos/use-ghas-with-ai-coding-agents/scan-for-secrets-with-github-mcp-server |
| **Claude Code deny + env scrub** | `Read(./.env)` deny; `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`. | Yes — code.claude.com |
| **Pipecat Cloud secret sets** | Deploy binds a **set name**. GET returns keys only. | Yes — docs.pipecat.ai |
| **Third-party MCP brokers (e.g. secr.dev)** | `secr.get` over MCP with an allowlist. Vendor product, not a standards body. Prefer 1Password/Infisical/Doppler/Vault unless you already run one. | Marketing site — not used as a requirement here |

There is still **no** safe pattern where the agent both **needs the raw value** and **must not see it**. If the bot process needs the key, inject it **below** the LLM. If the LLM would call `printenv`, deny that command.

---

## For this Pipecat × Scalekit laptop demo

Human (outside chat):

1. Scalekit Dashboard → copy credentials into 1Password (or Infisical/Doppler), **or** into a gitignored `.env` you type yourself.
2. Do not paste values into the agent.
3. Run the bot with `op run -- uv run bot.py` (or equivalent).
4. Deny agent reads of `.env`.

Agent:

1. Code uses `os.getenv`.
2. Repo has `.env.example` (names only) and `.env` in `.gitignore`.
3. Never log env. Never open `.env`.

This local demo still does **not** need Pipecat Cloud.
