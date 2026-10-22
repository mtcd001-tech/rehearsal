# Rehearsal — Devpost submission draft

> Draft for the Build, Ship, Shape: Amazon Developer Hackathon. Review every claim before pasting it into Devpost. Items marked **[fill in]** need the author's input. Deadline: **Friday, October 23, 2026, 12:00 p.m. PT (3:00 p.m. ET)**.

## Basics

- **Project name:** Rehearsal
- **Tagline:** Interview practice that quotes your own words back to you, names one thing to fix, and shows whether your retry fixed it.
- **Primary track:** Alexa+ (self-hosted MCP server, spec 2025-11-25 over Streamable HTTP, plus a simulated Alexa+ experience in a web app)
- **Mini challenges:** None claimed.
- **Repository:** **[fill in GitHub URL]** (public, MIT license detectable in the About section)
- **Demo video:** **[fill in YouTube/Vimeo URL]** (public, under 3 minutes)
- **Built with:** Python, FastAPI, Model Context Protocol Python SDK (`mcp` 1.30.0, FastMCP, Streamable HTTP), vanilla JavaScript, Web Speech Synthesis API, MediaRecorder and Web Audio APIs, OpenAI Realtime and Chat Completions APIs (optional path, unverified)

## Image gallery

Upload these from `docs/screenshots/` (real captures; captions are in that folder's README):

1. `1-practice-room.png`
2. `3-live-rule-check.png`
3. `4-retry-comparison.png`
4. `5-your-own-answer-compared.png`
5. `6-mcp-app-card.png`
6. `7-mobile.png`

## Inspiration

Behavioral interviews are hard for students applying to technical internships, especially when English is not their first language. The usual feedback is either a generic tip ("use STAR") or a single score that gives no clue about what to say differently. The most common problem in real answers is very specific: people say "we worked on it" and "it worked well," so the interviewer never hears what *they* did or how they knew it worked.

## What it does

- An illustrated virtual interviewer, Maya, asks a behavioral question and speaks it with the browser's speech synthesis. After a check, she can say the tip aloud, quoting your own words.
- You answer. In the sample you hear a realistic first answer; in practice mode you record yourself (audio stays in the browser) or type your answer.
- **Check my words** runs the `check_answer_text` MCP tool. It quotes your exact phrases and flags:
  - whether your own role is clear ("I" versus "we"),
  - concrete "I + action" phrases,
  - whether you said how you verified the result,
  - vague outcomes ("made it better", "worked well"),
  - filler words in the text,
  - numbers you should be ready to support,
  - reflection or honest limits,
  - and length.
  
  It picks one priority for the next try.
- You answer the same question again. **Compare first and latest take** runs `compare_answer_texts`, which shows which signals moved in the suggested direction, with before and after quotes. It says so plainly when nothing changed.
- **Optional live captions.** You can opt in to letting the browser's speech recognition draft your transcript while you record, so a spoken answer can be checked without typing. In Chrome this uses Google's online speech service, and the checkbox says so.
- **Practice history across sessions (opt-in).** *Save results to my progress* stores only signal labels and counts on your computer, never your words or audio. Next time, the app (or an assistant calling `get_practice_progress`) opens with your recurring priority, for example "your own role — moved toward the suggestion on 1 retry."
- **MCP App card.** The check tools are linked to an MCP Apps view (`ui://rehearsal/answer-check`, SEP-1865). Hosts that support MCP Apps can render the quoted findings as an interactive card instead of raw JSON. A local reference host at `/mcp-app-preview` shows the full handshake.
- No scores, no accent or personality judgments, no hiring predictions. Every quote is an exact substring of what you said, so evidence cannot be invented.
- An optional live mode (OpenAI Realtime voice over WebRTC, with the same MCP tools bridged as function calls) is implemented. It is **not verified end to end** because the available API key had no quota. The demo does not show it.

## How we built it

- **MCP server:** FastMCP from the official Python SDK, mounted on FastAPI, stateless Streamable HTTP with JSON responses. It negotiates protocol 2025-11-25. It ships server instructions that describe the coaching loop for an agent, and tool titles and annotations (the check tools are read-only, idempotent and closed-world).
- **Seven tools:**
  - `check_answer_text` and `compare_answer_texts`: deterministic, no key.
  - `get_practice_progress` and `save_practice_result`: local, opt-in history of derived signals only. Deleting history is deliberately an app action, not an agent tool.
  - `get_interview_brief`: session context.
  - `coach_latest_answer` and `compare_retry`: model-written, with exact-substring quote filtering, plus rule checks attached.
- **MCP Apps:**
  - The check tools declare `_meta.ui.resourceUri` and return `structuredContent`.
  - The `text/html;profile=mcp-app` resource implements the `ui/initialize` handshake, tool-input and tool-result notifications, size-changed, and host theming.
  - We wrote a small reference host to test it, because we had no third-party host available.
- **The web app is itself an MCP client:** its `/api/check`, `/api/compare-text` and `/api/tool` endpoints call the real MCP endpoint through the SDK's Streamable HTTP client. The browser therefore shows actual tool output, including the protocol version.
- **Local practice:**
  - MediaRecorder with a Web Audio level meter, a two-minute cap and four takes.
  - Typed takes when no microphone is available.
  - JSON export of your notes and check results.
- **Safety:**
  - The server binds to loopback and checks Host and Origin headers.
  - Sessions live in memory with expiry.
  - Live mode asks for explicit consent before any audio is sent, and the API key stays on the server.
- **Tests:**
  - 23 Python tests: rule checks, practice history, quote filtering, session handling, and HTTP plus real MCP integration.
  - Mocked browser-API tests for recording, typed takes, checks and reset.
  - Headless Chrome checks with Chrome's fake microphone device.

## Challenges

- **No API access during the build.** A minimal request returned `429 insufficient_quota`. So the coaching loop needed to work without any model. Deterministic rules turned out to be a better default for trust anyway: they never invent evidence.
- **MCP errors became HTTP 500.** Errors raised inside the MCP client context reached our web endpoints as an `ExceptionGroup`, so every tool error showed up as "Internal Server Error." See the friction log.
- **Honest labels.** Keeping the authored sample, the deterministic checks and the unverified AI path clearly separated in the UI took deliberate design.

## Accomplishments

- A complete practice loop that works offline with no key: question → answer → quoted evidence → one priority → retry → measured change.
- A real MCP server that a voice assistant could drive with the same loop, verified at protocol 2025-11-25, with context that carries across sessions without storing what the candidate said.
- No invented evidence: every quote shown is checked against the actual text.

## What we learned

- Useful interview feedback is mostly about specificity. Pointing at the exact phrase "we worked on the database" teaches more than any score.
- Agent-facing tools need instructions and honest annotations, not just function signatures.

## What's next

- Connect to Alexa+ when access is available, so the loop runs fully by voice.
- Verify the live AI path end to end with a working key.
- More question sets (data structures, system design talk-throughs), and history trends over time.
- Test with actual internship candidates, including non-native speakers, before claiming impact.

## Product feedback (required)

### Model Context Protocol — specification and Python SDK (`mcp` 1.30.0)

- **Used for:** the self-hosted coaching server (FastMCP, Streamable HTTP, stateless, JSON responses) and the client inside our own web backend.
- **What worked well:** a decorated Python function becomes a typed tool quickly. Streamable HTTP mounted cleanly into FastAPI. Protocol 2025-11-25 negotiated with no extra configuration. `instructions`, tool `title` and `ToolAnnotations` were easy to add.
- **What needs work:** error handling across the client boundary (friction entries 1 and 2). There is no app `version` parameter on `FastMCP(...)`, so `serverInfo.version` reports the SDK version, `1.30.0` (entry 3).
- **Onboarding:** reaching a working tool call took one short server plus the SDK client example. The error-handling behavior took longer to understand than the setup.
- **Would we build with it again?** Yes. It gives one well-defined surface that both our web app and a voice assistant can call.

### Alexa+ (track)

- **Used for:** target platform. We built the self-hosted MCP server path and a simulated Alexa+ experience.
- **What worked well:** the rules clearly allow a self-hosted MCP server or a simulation, so we could build without hardware.
- **What needs work:** entrants cannot connect a local MCP server to Alexa+ itself, so we could not test real voice turn-taking with our tools (entry 4).
- **Onboarding:** **[fill in from your own experience with the developer portal, if any]**
- **Would we build with it again?** Yes, if an Alexa+ test harness becomes available. Practice by voice is exactly the interaction this product needs.

### OpenAI Realtime API and Chat Completions (optional live path)

- **Used for:** optional live voice interviewer and AI coaching. Ephemeral client secrets keep the standard key on the server.
- **What worked well:** the WebRTC flow and client-secret design fit a browser app with a local backend.
- **What needs work:** we could not verify it. A minimal text request returned HTTP 429 `insufficient_quota`, and the Realtime client-secret request returned HTTP 500 `server_error` with the same key.
- **Would we build with it again?** Undecided until it can be verified.

### Browser APIs (Chrome): MediaRecorder, Web Audio, Speech Synthesis

- **What worked well:** fully local recording and playback with no upload.
- **What needs work:** Chrome's MediaRecorder WebM files report `duration = Infinity`, so the audio player shows no length until you seek (entry 5). Speech-synthesis voices vary by operating system.

## Friction log (optional; up to a 10% bonus)

Every entry below was observed during this build.

1. **Exceptions inside the MCP client context arrive as `ExceptionGroup`**
   - **Task:** return a tool's error message from our web endpoint.
   - **Steps:** called `ClientSession.call_tool` inside `streamable_http_client(...)` and `ClientSession(...)`, then raised `ValueError(result.content[0].text)` when `isError` was true.
   - **Expected:** our `ValueError` handler returns HTTP 400 with the message.
   - **Actual:** the exception left the async context wrapped in an `ExceptionGroup`. FastAPI returned HTTP 500 "Internal Server Error" for every tool error, for example "Session expired."
   - **Severity:** Medium. Users saw meaningless errors and the bug was silent in unit tests.
   - **Workaround:** keep the result, exit both contexts, then raise.
   - **Suggestion:** document this in the client quickstart, or unwrap single-exception groups in the SDK's context managers.
2. **Tool errors are plain text with a fixed prefix**
   - **Task:** show a tool's error to the user.
   - **Actual:** `CallToolResult.isError` is true and the text is `"Error executing tool compare_answer_texts: <message>"`.
   - **Severity:** Low.
   - **Workaround:** strip the prefix with a regular expression.
   - **Suggestion:** a structured error field (code plus message) separate from the display text.
3. **No server version setting in FastMCP**
   - **Task:** identify our server build to clients.
   - **Actual:** `initialize` reports `serverInfo.version = '1.30.0'`, the SDK's version. `FastMCP.__init__` has no `version` parameter.
   - **Severity:** Low.
   - **Workaround:** none yet.
   - **Suggestion:** add a `version` argument.
4. **No way to test a local MCP server with Alexa+**
   - **Task:** verify that our tools work in a real Alexa+ voice turn.
   - **Actual:** Alexa+ access is not available to entrants, so we built a web simulation.
   - **Severity:** High for this track.
   - **Workaround:** simulated experience plus MCP integration tests.
   - **Suggestion:** a public Alexa+ simulator or test console that can connect to a developer's Streamable HTTP MCP endpoint.
5. **MediaRecorder WebM duration is Infinity in Chrome**
   - **Task:** play back a local recording with a seek bar.
   - **Actual:** `audio.duration === Infinity` after `loadedmetadata`.
   - **Severity:** Low.
   - **Workaround:** seek to a very large time once, then back to zero.
   - **Suggestion (browser platform):** write duration metadata when recording stops.

6. **FastMCP silently omits `structuredContent` for `-> dict`**
   - **Task:** return `structuredContent` so an MCP Apps view can render tool results.
   - **Steps:** a tool annotated `-> dict` returned only text content. Adding `structured_output=True` then failed at startup with `InvalidSignature: ... return type <class 'dict'> is not serializable for structured output`.
   - **Expected:** a plain `dict` is treated as an object.
   - **Actual:** with no annotation it was silently text-only; with the flag it raised an error.
   - **Severity:** Low to Medium. MCP Apps views depend on `structuredContent`.
   - **Workaround:** annotate `-> dict[str, Any]` and pass `structured_output=True`.
   - **Suggestion:** accept a bare `dict` as `dict[str, Any]`, or warn when an MCP Apps-linked tool returns no `structuredContent`.
7. **No reference host for testing MCP Apps views locally**
   - **Task:** verify our `ui://` view before submission.
   - **Actual:** we had no MCP Apps-capable host, so we wrote a minimal host page to run the handshake.
   - **Severity:** Medium.
   - **Workaround:** `/mcp-app-preview` in this repo.
   - **Suggestion:** an official browser-based MCP Apps inspector or test host.

## Feature requests (optional)

- **Alexa+ developer test console for self-hosted MCP servers.** Lets track entrants verify real voice behavior. Priority: Critical.
- **Structured tool errors in the MCP Python SDK.** Lets clients show clean messages without parsing strings. Priority: Important.
- **Browser-based MCP Apps test host or inspector.** Lets view authors debug the handshake without a full chat client. Priority: Important.
- **`version` argument for FastMCP.** Lets clients identify server builds. Priority: Nice-to-have.

## What was built during the submission period

All of Rehearsal (`interview/`) was created during the submission period, in October 2026. The `trace/` folder is a separate earlier experiment from the same week and is not part of this submission.
