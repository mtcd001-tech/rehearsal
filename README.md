# Rehearsal — interview practice that shows you exactly what to change

Rehearsal is an interview-practice room for technical-internship candidates, including non-native English speakers. An illustrated interviewer asks a behavioral question, you answer out loud or in writing, and you get feedback tied to the **exact words you used**, one priority to fix, and a side-by-side check of whether your retry actually changed.

The coaching engine is a self-hosted **MCP server** (spec **2025-11-25**, Streamable HTTP). Its core tools are deterministic and need **no API key**, so any MCP client — or a voice assistant such as Alexa+ — can call them. The browser app is a simulated Alexa+-style practice experience built on those same tools.

![Rehearsal: authored coaching above, live check_answer_text MCP results below](docs/screenshots/2-coaching.png)

> Hackathon track: **Alexa+** — self-hosted MCP server, plus a simulated Alexa+ experience in a web app.

## What works today, and what does not

| Part | Status |
|---|---|
| Authored sample interview (animated interviewer, browser speech, coaching, retry, comparison) | Works. The sample answers and the main coaching card are **written by hand** and labelled as such. |
| Rule checks on the sample answers | Works. Computed live by the MCP tools `check_answer_text` and `compare_answer_texts` every time the sample runs. |
| Practice with your own answer: record audio locally, or type an answer | Works. Audio never leaves the browser tab. |
| Optional browser captions while recording (opt-in) | Implemented and unit-tested with a mocked recognizer; real speech results not yet verified. |
| Check my words / compare first and latest take | Works. Your typed text goes only to the local server; deterministic rules, no AI model, no scores. |
| Opt-in practice history across sessions (signal labels and counts only, on this computer) | Works. An agent can open a session with last time's focus via `get_practice_progress`. |
| MCP server (7 tools) over Streamable HTTP, protocol 2025-11-25 | Works and is covered by integration tests. |
| MCP Apps view (`ui://rehearsal/answer-check`, SEP-1865) for the check tools | Works in the included local reference host at `/mcp-app-preview`. Not yet tried in a third-party MCP Apps host. |
| Live AI voice interview (OpenAI Realtime over WebRTC) and AI typed practice | Implemented but **not verified end to end** — the available API key had no quota. Treat as unverified. |

## Run it (about 2 minutes)

Requires Python 3.11+ and a recent Chrome or Edge.

**Windows (PowerShell)**

```powershell
git clone <this repository> rehearsal
cd rehearsal
python -m venv .venv
.venv\Scripts\python -m pip install -r interview\requirements.txt
.venv\Scripts\python interview\server.py
```

**macOS / Linux**

```bash
git clone <this repository> rehearsal && cd rehearsal
python3 -m venv .venv
.venv/bin/python -m pip install -r interview/requirements.txt
.venv/bin/python interview/server.py
```

Open **http://127.0.0.1:8766**. No API key or account is needed.

1. **Experience the sample** → *Play sample answer* → *See the coaching*. Under the authored coaching card, a panel shows what the `check_answer_text` MCP tool found in the sample answer, with quotes.
2. *Try that answer again* → *Play improved answer*. The comparison shows the authored before/after pairs and a panel computed by `compare_answer_texts`.
3. **Practice my own answer**. Record a take (or choose *No microphone? Type an answer*), write what you said, and press **Check my words**. Add a second take and press **Compare first and latest take**. Optionally press **Save results to my progress**; next time, the history panel suggests your recurring focus.

## Use the MCP server from any MCP client

While the server runs, the endpoint is **`http://127.0.0.1:8766/mcp`** (Streamable HTTP, stateless, JSON responses).

| Tool | Needs API key | What it does |
|---|---|---|
| `check_answer_text(answer, question?)` | No | Wording checks with exact quotes: your own role (I vs we), concrete I-actions, how you verified the result, vague outcomes, fillers, numbers you should be ready to support, reflection, length. Returns one priority to work on. |
| `compare_answer_texts(before, after)` | No | Which of those signals moved in the suggested direction between two takes, with before/after quotes. Says so plainly when nothing changed. |
| `get_practice_progress()` | No | Saved sessions, recurring priorities, and a suggested focus, so a voice assistant can start with context. |
| `save_practice_result(question, first_answer, retry_answer?)` | No | Saves only signal labels, statuses, counts, and the comparison summary — never answer text or audio. Called only when the candidate asks. |
| `get_interview_brief(session_id)` | No | Session context and transcript for an agent. |
| `coach_latest_answer(session_id)` | Yes | Model-written coaching; quotes are filtered so only exact substrings of the real answer survive. Also attaches the rule checks. |
| `compare_retry(session_id)` | Yes | Model-written retry comparison with the same quote filter. |

### MCP Apps view

`check_answer_text` and `compare_answer_texts` carry `_meta.ui.resourceUri = "ui://rehearsal/answer-check"` and return `structuredContent`. The resource (`text/html;profile=mcp-app`) is a self-contained card that speaks the MCP Apps postMessage protocol (`ui/initialize`, `ui/notifications/tool-input`, `ui/notifications/tool-result`, `ui/notifications/size-changed`), adapts to the host theme, and needs no network access. Hosts without MCP Apps still get the full JSON text result.

Open **http://127.0.0.1:8766/mcp-app-preview** to see it rendered by a minimal reference host included in this repo: it reads the resource over MCP, loads it in a `sandbox="allow-scripts"` iframe, forwards the real tool result, and logs every JSON-RPC message.

### Try it from Python

Quick check with the official Python SDK (already installed by the requirements):

```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client('http://127.0.0.1:8766/mcp') as (read, write, _):
        async with ClientSession(read, write) as session:
            print((await session.initialize()).protocolVersion)        # 2025-11-25
            result = await session.call_tool('check_answer_text', {'answer': 'We fixed the bug and it worked well.'})
            print(result.content[0].text)

asyncio.run(main())
```

## Why the checks are rules, not a model

Interview feedback is only useful if you can trust it. Every quote Rehearsal shows is sliced from your own words, so evidence cannot be invented. The rules never produce a score, never comment on accent or personality, and say "text only, not an audio fluency measurement" where that matters. When the AI coaching path is enabled, its quotes go through the same exact-substring filter.

The rules are intentionally simple English word lists. They can miss things or misfire (for example, "profiled" counts as checking your work). They are prompts for a better retry, not a judgment of the answer.

## Privacy

- Sample mode sends nothing anywhere except to the local server for the rule-check panels.
- Local practice keeps audio in the browser tab. Only text you choose to check is sent, and only to `127.0.0.1`.
- Exception you must opt into: *Draft a transcript while I speak* uses the browser's speech recognition. In Chrome that sends your audio to Google's speech service. It is off by default and labelled on screen.
- The server binds to loopback, rejects other hosts and origins, and keeps session data in memory only.
- Practice history is written only when you press *Save results to my progress*, to `interview/data/practice_history.json` (git-ignored), and contains signal labels and counts, not your words. *Clear my history* deletes the file.
- The optional live AI path sends audio and transcript to OpenAI and asks for consent first. It is off unless you configure a key (`interview/.env`, see `interview/.env.example`).

## Tests

With the server running (set `INTERVIEW_PORT` if you started it on another port):

```powershell
cd interview
..\.venv\Scripts\python -m unittest test_interview test_checks test_history -v
node test_practice.cjs
```

23 Python tests (rule checks, practice history, quote filtering, session handling, HTTP and real MCP integration) and mocked browser-API tests for recording, typed takes, checks, and reset. Model responses are mocked; no paid calls are made.

## Repository layout

| Path | Contents |
|---|---|
| `interview/` | Rehearsal: FastAPI app, MCP server, rule checks, sample scenario, web client, tests |
| `interview/README.md` | Detailed behavior, limits, and verification notes |
| `SUBMISSION.md`, `DEMO.md` | Hackathon submission text, product feedback, friction log, demo script |
| `trace/` | An earlier, paused prototype (code-tracing visualizer). Not part of this submission. |
| `HANDOFF.md`, `WORK_LOG.md`, `AGENTS.md` | Development handoff notes and log |

## Prior art and honest positioning

Interview-roleplay tools already exist (for example [Yoodli](https://yoodli.ai/use-cases/interview-preparation)). Rehearsal's angle is narrower: evidence you can verify, one change at a time, and a retry comparison that shows whether the change happened — exposed as an MCP server so a voice assistant can run the same loop. Learner impact has not been measured yet.

## License

MIT — see [LICENSE](LICENSE).
