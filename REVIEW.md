# Code review — pipecat-x-sample

Two axes. Do not merge them.

**Fixed point:** working tree vs spec. This folder is untracked in `feedback-syndicate`. There is no git SHA. `git diff HEAD` for this directory is empty because the files are `??`.

**Spec sources:** SK-1162, `TRACKER.md`, `README.md`, `AGENTS.md`, plus the identity contract in this task (TEST_IDENTIFIER, `connection_name`, one tool, no token to the LLM).

**Standards sources:** `AGENTS.md`, `TRACKER.md`, parent `Claude.md`, Fowler smell baseline.

**Tree reviewed:** `bot.py`, `scalekit_calendar.py`, `smoke_calendar.py`, `roundtrip.py`, `tests/test_scalekit_calendar.py`, `pyproject.toml`, `.env.example`, `.gitignore`, `README.md`, `TRACKER.md`, `AGENTS.md`, `RESEARCH.md`.

---

## Standards

### Hard — documented standard

**1. `TRACKER.md` local table is false.**  
`AGENTS.md`: “Keep state in `TRACKER.md`.” `TRACKER.md` itself: write status here after any session that changes it.

The local table still says:

| Claim | Disk |
| -- | -- |
| `bot.py` Draft. Not run. | File exists; `__pycache__/bot.cpython-312.pyc` exists |
| `pyproject.toml` `uv sync` not run | `.venv/` and `uv.lock` exist (`pipecat-ai==1.11.0`) |
| `.env` Missing | `.env` exists (gitignored) |
| Run Not verified | True for the voice bot; the other rows are stale |

**2. Proof scripts still copy the Scalekit call.**  
`Claude.md` §2: “Minimum code that solves the problem.” `Claude.md` §3: every changed line should trace to the request.

`scalekit_calendar.list_calendar_events` is now the bot path (`bot.py` 32, 131–139). `smoke_calendar.py` and `roundtrip.py` still construct `ScalekitClient` and call `actions.execute_tool` themselves. `_env` is copied in four files.

### Judgement — smell baseline

**Duplicated Code** — same execute_tool shape in `smoke_calendar.py` 60–66 and `roundtrip.py` 37–49. Extract already exists. Call it.

**Speculative Generality** — `_speakable` in `scalekit_calendar.py` 69–86 still JSON-round-trips and tries `.items()`. The spec only needs `response.data` plus token strip. `_TOKEN_KEYS` includes generic `token` / `bearer`.

**Speculative Generality** — `pyproject.toml` lower bound is `pipecat-ai>=0.0.95`. The code needs 1.x (`PipelineWorker`, `WorkerRunner`, `Service.Settings`). `.gitignore` drops `uv.lock`, so a later `uv sync` can resolve a different API.

Skip: daily/twilio transport lambdas. `TRACKER.md` cites `07-function-calling.py`, which uses the same map. Repo citation wins over the smell.

---

## Spec

### (a) Missing or partial

**Voice bot is not proven.**  
SK-1162 Next / `TRACKER.md` 30: “Status stays Todo until the bot runs.”  
`README.md` 41–44: `uv run bot.py` then open `http://localhost:7860/client`.  
That path is not recorded as run. Smoke and roundtrip are not in README.

**Local speech fallback does not match README.**  
`README.md` 34: without Deepgram and Cartesia, “the bot uses local Whisper and Kokoro.”  
`bot.py` 104–109 always uses `WhisperSTTServiceMLX`. That extra is macOS arm64. RESEARCH.md says the CPU path is `WhisperSTTService`.

**`roundtrip.py` does not prove the bot contract.**  
It says it proves the same identity contract (`roundtrip.py` 1–3). It then:

- ignores the LLM tool arguments and lists “today” (`roundtrip.py` 111 vs 29–51)
- sends raw `response.data` to the LLM (`roundtrip.py` 118), not `list_calendar_events` / `_without_tokens`

### (b) Scope creep

`smoke_calendar.py`, `roundtrip.py`, `tests/`, `RESEARCH.md` are extra vs SK-1162 “build a sample voice agent.” They are local proof, not a Pipecat org PR. Acceptable for this play area. Not a fail.

Daily and Twilio transports are extra vs README’s `:7860/client`. They match the cited Pipecat example. Not a fail.

### (c) Implemented, but wrong or incomplete

**Token strip is on the bot path only.**  
Spec / `AGENTS.md` 11: “The LLM never sees an OAuth token.”  
`list_calendar_events` strips token keys and is what `bot.py` returns to `result_callback`. Good.  
`roundtrip.py` still dumps unstripped Scalekit data into the chat completion. That is the other LLM path in this folder.

**Identity call shape is right in the bot helper.**  
Python `connection_name`, not Node `connector`. `tool_name="googlecalendar_list_events"`. `identifier=TEST_IDENTIFIER`. Matches TRACKER 46–47 and the Python SDK.

**No Nina / Slack / Pipecat org PR in this tree.** Matches `AGENTS.md` 8–10.

---

## Summary

Standards: 2 hard, 3 judgement. Worst: `TRACKER.md` is out of date (`AGENTS.md` keep-state rule).

Spec: 3 partial, 1 wrong-path. Worst: voice bot is still unrun, which is the SK-1162 done condition.

No overall winner across axes.
