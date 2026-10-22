> **Paused earlier prototype.** Trace is not the hackathon submission. The active project is Rehearsal — see the [repository README](../README.md).

> **Agent starting point:** Read [HANDOFF.md](HANDOFF.md), [AGENTS.md](AGENTS.md), and [WORK_LOG.md](WORK_LOG.md) first. The active project is **Rehearsal in `interview/`**; this root README describes the paused Trace prototype.

# Trace

**See where your reasoning and your code diverge.**

Trace is a local Python execution explorer with an MCP-controlled visual debugger. It records real Python execution, displays the call stack and object identities, and navigates to evidence behind index errors and shared mutable lists.

## Run on Windows

Requires Python 3.11 or later. No API key, Amazon device, or cloud account is required.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-lock.txt
.venv\Scripts\python server.py
```

Open **http://127.0.0.1:8765**. Keep the terminal running. Alternatively, run `start.ps1` from PowerShell.

On macOS/Linux, substitute `.venv/bin/python` for `.venv\Scripts\python`. Install from `requirements.txt` there; the Windows lock includes platform-specific dependencies.

## Three walkthroughs

1. **The disappearing subsets:** choose “Find shared references.” Several saved answers point to the same list. Step forward to watch `path.pop()` mutate the object all those answers reference. Select “Compare with a correction” to run `path.copy()` instead and check against an explicit expected result.
2. **One step too far:** choose “Show the error.” The canvas jumps to the actual `IndexError` and displays index 4 against four valid slots, 0–3. Compare the corrected loop.
3. **Inside the call stack:** watch five factorial calls descend, then use “Next return” to inspect the unwind.

Edit the source to run your own short program. Use the slider, playback, arrow buttons, or keyboard left/right arrows to navigate. A **line** event shows state **before** that line executes. Call, return, and exception events have their own semantics and labels.

## Alexa+ hackathon track

This is an **Alexa+ experience simulation**, not a deployed Alexa integration and not Amazon's private simulator. The working MCP server exposes:

- `trace_python(source)`: execute and retain a trace; return its ID and result summary.
- `inspect_step(run_id, step)`: retrieve recorded frames, object memory, and exceptions.
- `navigate_trace(run_id, target, current_step, variable)`: locate an error, repeated references, the next variable change, a return, or a timeline position.

Endpoint: **http://127.0.0.1:8765/mcp**. Transport: **Streamable HTTP**. Verified negotiated protocol: **2025-11-25**. An MCP client can discover and call these tools directly.

The web command panel connects as an MCP client through the same HTTP endpoint. It currently uses a **deterministic intent router**, not an LLM. Supported phrases include “show the error,” “find shared references,” “when did path change,” “next return,” “start,” “end,” “next,” and “previous.” Unsupported questions are explicitly reported. There is no fabricated model output, voice recognition, or automatic general-purpose bug fixing. The two correction buttons are authored example patches and are labeled as such.

## Architecture

```text
Browser -> FastAPI /api/run -> subprocess -> CPython sys.settrace
Browser -> /api/ask -> deterministic intent router
                    -> MCP Streamable HTTP client
                    -> navigate_trace -> recorded evidence -> canvas position
External MCP client -> /mcp -> trace_python / inspect_step / navigate_trace
```

Object identities remain stable across a run. The serializer records heap references instead of recursively duplicating shared lists, including cycles. Call records have parent IDs and entry/exit events. No LLM generates execution states.

## Scope and execution limits

- Trusted local snippets only. **This is not a hardened sandbox. Do not expose this service publicly or run untrusted code.**
- The server binds to loopback and checks Host/Origin. These are defense-in-depth, not process isolation.
- A child process gets a four-second execution timeout; traces stop at 600 events. Imports, classes, async, generators, exception handling, and most attribute access are rejected.
- Programs are limited to 12,000 source characters. Snapshot output is truncated to 4,000 characters; each collection shows at most 60 items, with bounded nesting.
- No OS memory quota is implemented; expressions can allocate memory before a timeout. This is one reason this build stays local.
- Variable-change navigation compares the innermost visible variable by name; it is not full data-flow analysis or a causal proof. Shared references are legal Python, not automatically a bug.
- Runs are held in memory, with only the most recent 24 retained; restarting the server clears them.
- No LeetCode integration, scraped questions, user accounts, analytics, paid services, or hosted deployment.
- Google Fonts is an optional network request for typography; system font fallbacks work offline.

## Verification

Start the server, then in another terminal:

```powershell
.venv\Scripts\python -m unittest test_trace -v
node --check static/app.js
```

The tests check actual alias identities, independent copied lists, exact out-of-bounds access, recursive call relationships, line-event timing, cycles, rejected syntax, event limits, HTTP endpoints, origin rejection, and MCP initialization/tool execution. Browser visual QA remains pending because this build environment exposed no browser automation surface.

## Prior art and positioning

[Python Tutor](https://pythontutor.com/) already visualizes execution, frames, and references. Trace does **not** claim to invent execution visualization. Its prototype focus is evidence-directed conversational navigation plus a before/after learning loop. Differentiation and educational effectiveness still need user validation.

## Submission preparation

See `SUBMISSION.md` for draft Devpost copy and `DEMO.md` for a recording script. These are drafts, not evidence of a submitted entry. The GitHub repository, public demo video, and final Devpost submission are still to be completed. No AWS Builder or Open Source mini challenge eligibility is claimed.
