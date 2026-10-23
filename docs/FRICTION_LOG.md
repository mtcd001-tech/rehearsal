# Rehearsal: friction log

Every entry was observed while building [Rehearsal](https://github.com/mtcd001-tech/rehearsal) for the Build, Ship, Shape: Amazon Developer Hackathon, Alexa+ track, in October 2026.

Severity scale: **High** = blocked a goal; **Medium** = broke a feature until worked around; **Low** = an annoyance.

---

## 1. MCP Python SDK: tool errors become `ExceptionGroup`, so our users saw HTTP 500

- **Task:** return an MCP tool's error message (for example, "Session expired") from our FastAPI endpoint as HTTP 400.
- **Steps:**
  1. Opened `streamable_http_client(url)` and `ClientSession(...)` as nested `async with` blocks.
  2. Called `call_tool`.
  3. When `result.isError` was true, raised `ValueError(result.content[0].text)` inside the blocks.
- **Expected:** our `ValueError` exception handler returns HTTP 400 with the readable message.
- **Actual:** the exception left the client's anyio task group wrapped in an `ExceptionGroup`. FastAPI's `ValueError` handler didn't match it, so every tool error reached the browser as "Internal Server Error". Unit tests didn't catch it, because they called the tool functions directly.
- **Severity:** Medium.
- **Workaround:** store the result, let both context managers exit, then raise.
- **Suggestion:** document this in the client quickstart, or unwrap single-exception groups raised by user code inside `ClientSession` / `streamable_http_client`.

## 2. MCP Python SDK: tool errors are plain text with a fixed prefix

- **Task:** show a tool's error to the user cleanly.
- **Steps:** a tool raised `ValueError('The retry is identical…')`; the client read `CallToolResult`.
- **Expected:** a structured error, or the original message.
- **Actual:** `isError=True`, and the content text is `"Error executing tool compare_answer_texts: <message>"`.
- **Severity:** Low.
- **Workaround:** strip the prefix with a regular expression before showing it.
- **Suggestion:** a structured error field (code plus message) kept separate from the display text.

## 3. FastMCP: no way to set the server's version

- **Task:** identify our server build to MCP clients.
- **Steps:** created `FastMCP('Rehearsal interview coach', …)`, then inspected the `initialize` response from a client.
- **Expected:** a `version` argument, or a way to set `serverInfo.version`.
- **Actual:** `serverInfo.version` reports `1.30.0` (the SDK's version), and `FastMCP.__init__` has no `version` parameter.
- **Severity:** Low.
- **Workaround:** none.
- **Suggestion:** add `version=` to `FastMCP(...)`.

## 4. FastMCP: `structuredContent` is silently missing for a bare `-> dict`

- **Task:** return `structuredContent` so an MCP Apps view can render tool results.
- **Steps:**
  1. Annotated the tool `-> dict` and called it: the result had text content only.
  2. Added `structured_output=True`.
- **Expected:** a plain `dict` is treated as a JSON object.
- **Actual:** with no flag it was silently text-only; with the flag, startup failed with `InvalidSignature: return type <class 'dict'> is not serializable for structured output`.
- **Severity:** Medium (MCP Apps views depend on `structuredContent`).
- **Workaround:** annotate `-> dict[str, Any]` and pass `structured_output=True`.
- **Suggestion:** accept a bare `dict` as `dict[str, Any]`, or warn when a tool linked to a UI resource returns no `structuredContent`.

## 5. MCP Apps: no reference host to test a `ui://` view locally

- **Task:** verify our MCP Apps card (`ui://rehearsal/answer-check`, `text/html;profile=mcp-app`) before submitting.
- **Steps:** looked for a host or inspector able to load the resource and run the `ui/initialize` → `tool-input` → `tool-result` handshake.
- **Expected:** an official browser-based test host or inspector.
- **Actual:** none was available to us.
- **Severity:** Medium.
- **Workaround:** wrote our own minimal reference host (`/mcp-app-preview`), with a sandboxed iframe and a JSON-RPC message log.
- **Suggestion:** an official MCP Apps inspector or test host.

## 6. Alexa+: no way to test a self-hosted MCP server with Alexa+

- **Task:** check that our MCP tools work inside a real Alexa+ voice conversation.
- **Steps:** followed the track's guidance to the MCP getting-started docs, built a Streamable HTTP server (protocol 2025-11-25), and looked for a way to connect it to Alexa+.
- **Expected:** a developer console or simulator that connects to a developer's MCP endpoint.
- **Actual:** Alexa+ access is not available to entrants, so no real voice turn could be tested.
- **Severity:** High for this track.
- **Workaround:**
  - a simulated voice experience in the web app;
  - MCP integration tests;
  - a scripted terminal agent (`agent_sim.py`) that drives the tools in an assistant-style turn order.
- **Suggestion:** a public Alexa+ simulator or test console that accepts a developer's Streamable HTTP MCP URL.

## 7. Gemini API: Google Search grounding returns 429 while text generation works

- **Task:** company research with Google Search grounding (company and role only).
- **Steps:** one request with a public company and role, no retries; the same key's plain `generateContent` text request succeeded minutes earlier.
- **Expected:** grounded results, or a clear message about grounding quota or eligibility.
- **Actual:** HTTP 429 on repeated days, while ordinary text calls on the same key worked.
- **Severity:** Medium; the optional research feature couldn't be verified live.
- **Workaround:**
  - made research optional;
  - the interview works from the user's own setup;
  - no automatic retries on 429.
- **Suggestion:** a distinct error, or quota visibility for grounding versus generation, so developers can tell "grounding not available on this tier" from "rate limited".

## 8. Gemini API: transient HTTP 503 on the post-interview review

- **Task:** generate the debrief after a real interview.
- **Steps:** a live interview with a physical microphone completed; the review request was sent once.
- **Expected:** a review, or a retry hint.
- **Actual:** HTTP 503 (model overloaded); our first version showed a misleading "check API access and configuration" message.
- **Severity:** Medium; it was the user's first real run.
- **Workaround:**
  - bounded retries (up to 3 attempts, 2 s and 5 s backoff, `Retry-After` honoured, capped at 10 s) for 500/502/503/504 and network errors only, never 429;
  - a clearer "temporarily unavailable, nothing was lost" message;
  - a *Try analysis again* button.
- **Suggestion:** document recommended retry behaviour for 503 in the `generateContent` docs.

## 9. Chrome MediaRecorder: WebM duration is `Infinity`

- **Task:** play back a local practice recording with a working seek bar.
- **Steps:** recorded with `MediaRecorder` (`audio/webm;codecs=opus`), created a blob URL, and loaded it into `<audio>`.
- **Expected:** a finite `duration` after `loadedmetadata`.
- **Actual:** `audio.duration === Infinity`, so the player showed no length.
- **Severity:** Low.
- **Workaround:** seek to a very large time once, then back to 0, after which the duration becomes finite.
- **Suggestion (browser platform):** write duration metadata when recording stops.

---

## Feature requests

| Request | Why it matters | Priority |
|---|---|---|
| Alexa+ developer test console for self-hosted MCP servers | Lets track entrants verify real voice behaviour | Critical |
| Structured tool errors in the MCP Python SDK | Clean user-facing errors without string parsing | Important |
| Browser-based MCP Apps test host or inspector | Debug `ui://` views without a full chat client | Important |
| Clear grounding quota and eligibility errors in the Gemini API | Tell "not available" apart from "rate limited" | Important |
| `version` argument for FastMCP | Identify server builds to clients | Nice-to-have |
