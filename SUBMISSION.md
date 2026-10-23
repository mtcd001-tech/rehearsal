# Rehearsal — Devpost submission draft

> Draft for the Build, Ship, Shape: Amazon Developer Hackathon. Review every claim before pasting it into Devpost. Items marked **[fill in]** need the author's input. Deadline: **Friday, October 23, 2026, 12:00 p.m. PT (3:00 p.m. ET)**. Verification status in this file is accurate as of October 22, 2026, evening ET. If you verify something new (for example, a full interview with your own microphone), update the "Verification status" section.

## Basics

- **Project name:** Rehearsal
- **Tagline:** A timed mock interview with a voice interviewer who follows up like a real one — then feedback that quotes your own words and shows exactly what to change.
- **Primary track:** Alexa+ (self-hosted MCP server, spec 2025-11-25 over Streamable HTTP, plus a simulated Alexa+-style voice experience in a web app)
- **Mini challenges:** None claimed.
- **Repository:** https://github.com/mtcd001-tech/rehearsal (public, MIT license)
- **Demo video:** **[fill in YouTube/Vimeo URL]** (public, under 3 minutes)
- **Built with:** Python, FastAPI, Model Context Protocol Python SDK (`mcp` 1.30.0, FastMCP, Streamable HTTP), Gemini API (Live API for the voice interview; `generateContent` for review, questions, coaching and Google Search–grounded research), `websockets`, vanilla JavaScript, Web Audio (AudioWorklet), MediaRecorder, Web Speech Synthesis

## Image gallery

Upload from `docs/screenshots/`, in this order. All are real captures; captions are in that folder's README.

1. `01-home.jpg`
2. `04-interview-room.jpg`
3. `03-consent.jpg`
4. `02-setup.jpg`
5. `06-live-rule-check.png`
6. `07-retry-comparison.png`
7. `09-mcp-app-card.png`
8. `08-mobile.png`

## Inspiration

Behavioral interviews are hard for students applying to technical internships, especially when English is not their first language. A list of questions or a generic tip such as "use STAR" can leave a candidate unsure what to change in their own answer. We wanted to practice the harder part: responding when an interviewer follows up on what you just said.

One problem we designed for is vague ownership and evidence. People say "we worked on it" and "it worked well," so the interviewer never hears what *they* did or how they knew it worked.

## What it does

**1. A timed mock interview, hands-free.**

- Set up your target company, role, job description, resume (PDF/DOCX/TXT, extracted locally), round, length and skills to work on.
- Press *Enter interview room*, choose 5, 15 or 30 minutes, and consent.
- Maya, the interviewer, asks questions out loud and follows up on what you actually said. Turn-taking is automatic: there are no Record or Next buttons, and you can interrupt her.
- A countdown and the server both enforce the length. *End interview* is always available.
- **It feels like a video call.** An optional self-view shows your own camera in the corner, mirrored. It stays on your screen only: video is never recorded, uploaded or sent to Google.
- Maya feels present:
  - her mouth moves with the audio she is actually speaking;
  - her gaze shifts naturally;
  - she looks at you and nods slightly while you talk.
- No coaching appears during the interview, just like the real thing.

**2. A debrief after the interview, not during it.**

- When the interview ends, the microphone stops and a transcript-based debrief appears:
  - a summary;
  - what to keep doing, and the top priorities;
  - structure, clarity and technical reasoning;
  - each answer, with a quoted line from your own transcript, how to improve it, and a clearer version to fact-check.
- **Why Maya asked that.** For each follow-up, the debrief shows three things: **You said** (your exact words), **Still unclear** (what that answer left open, such as your own contribution or how you measured it), and **So Maya asked** (her actual follow-up). It teaches *why* a polished-sounding answer still draws a follow-up. Both quotes must appear verbatim in adjacent turns of the transcript, or the note is dropped. It is labelled as a practice explanation reconstructed from the transcript, not a real recruiter's reasoning.
- Quotes are filtered so only exact text from your transcript survives.
- There are no scores and no pronunciation, accent, personality or hiring judgments. With no transcript, no assessment is shown.
- You can download the transcript and review.

**Pressure Replay: put the feedback into practice.**

After the interview, choose a moment backed by a quote from one actual answer. In a short voice replay, Maya repeats the original question and then changes one condition in a follow-up. The app compares exact before/retry evidence and evaluates the follow-up separately. It can report no demonstrated improvement; there are no invented percentage scores. The original debrief is preserved. The comparison also says whether the retry **resolved** what the original answer left unclear (yes, partly, no, or unclear) and names one question still worth asking. An expandable wording comparison uses the existing MCP tool.

Synthetic live verification passed for the original question, two spoken answers, changed-condition follow-up, automatic end and Gemini comparison. New replay UI and physical-microphone flow still need user verification; do not describe the synthetic test as a real user demo.

**3. Single-answer practice and the retry loop.**

- Practice one question at a time: built-in questions, or one generated from your setup.
- Record your answer. Gemini can transcribe it and give feedback, a retry focus and a suggested draft with prompts for missing details.
- Ask for a follow-up question, or practice the same question again.
- Typed answers work too.

**4. A deterministic coaching layer as MCP tools, with no key needed.**

- `check_answer_text` quotes your exact words and flags:
  - "we" without "I";
  - missing concrete actions;
  - no word on how you verified the result;
  - vague outcomes ("made it better");
  - fillers in the text;
  - numbers you should be ready to support;
  - missing reflection;
  - length.
- It picks one thing to fix. `compare_answer_texts` shows which of those signals actually moved between your first take and your retry, and says so when nothing did.
- Practice history across sessions is opt-in and stores counts only, never your words.
- The check tools also render as an **MCP Apps** card (`ui://rehearsal/answer-check`, SEP-1865).

**5. A no-key authored demo.**

- An authored sample interview, clearly labelled as written by hand, shows the whole loop without any account or key.
- The rule-check panels in that demo are computed live by the MCP tools.

## How we built it

- **Live interview:**
  - `live_interview.py` bridges the browser to the Gemini Live API over a same-origin WebSocket.
  - The browser captures mono 16 kHz PCM with an AudioWorklet and plays Maya's native 24 kHz audio.
  - The server validates the local origin, bounds audio packets and transcript size, enforces the deadline, and enables context compression and session resumption for long sessions.
  - It captures input and output transcriptions and refuses review requests until the session has ended.
  - No raw audio is stored.
  - The optional self-view is a separate, video-only `getUserMedia` stream attached to a local `<video>` element. It never touches the WebSocket.
  - Maya's lip movement comes from an `AnalyserNode` on her actual output audio, and the listening state comes from microphone energy.
- **MCP server:**
  - FastMCP from the official Python SDK, mounted on FastAPI, with stateless Streamable HTTP. It negotiates protocol 2025-11-25.
  - It ships server instructions describing the practice loop for an agent, plus tool titles and annotations; the check tools are read-only and idempotent.
  - There are seven tools:
    - `check_answer_text` and `compare_answer_texts` (deterministic);
    - `get_practice_progress` and `save_practice_result` (opt-in history of derived counts; deleting history is deliberately an app action, not an agent tool);
    - `get_interview_brief`;
    - `coach_latest_answer` and `compare_retry` (Gemini-written, with exact-substring quote filtering).
  - The web app is itself an MCP client of these tools. `interview/agent_sim.py` is a scripted terminal agent (not an LLM) that runs the loop through real MCP calls, in the turn order an Alexa+ conversation would use.
- **MCP Apps:**
  - The check tools declare `_meta.ui.resourceUri` and return `structuredContent`.
  - The `text/html;profile=mcp-app` view implements the `ui/initialize` handshake, tool-input and tool-result notifications, size-changed, and host theming.
  - We wrote a small reference host (`/mcp-app-preview`) to test it.
- **Gemini `generateContent`:**
  - A shared JSON-schema helper powers recorded-answer review (audio in), tailored questions and follow-ups, text coaching and the post-interview debrief.
  - Company research uses Google Search grounding with company and role only, then a separate synthesis call. It produces cited sources, and uncited results are rejected.
- **Privacy and safety:**
  - Loopback-only server with Host and Origin checks.
  - Sessions live in memory with expiry.
  - Explicit consent before anything is sent to Google, and the key stays on the server.
  - The resume is extracted locally in a time-limited subprocess, and the file is not kept.
- **Tests:**
  - 76 Python tests, with providers mocked: schema validation, citations, resume parsing, the Live session lifecycle, review gating, the rule checks, history, and real local MCP integration.
  - 11 JavaScript suites with mocked browser and media APIs, including camera opt-in, release and denial: the AudioWorklet resampler, timed ending, microphone cleanup, late permission, stale results and recovery.

## Verification status (be precise in the video and on Devpost)

| Part | Status |
|---|---|
| Deterministic MCP tools, MCP Apps view, authored demo | Verified in a real browser and by integration tests. |
| Gemini Live interview | **Verified with a physical microphone** (author's run, Oct 22): Maya spoke, heard the answers, asked follow-ups on what was said, and the transcript was captured. Earlier synthetic-speech tests passed too. **A full 30-minute run has not been verified.** |
| Pressure Replay | Actual Gemini Live run with synthetic speech and evidence comparison passed; new browser and physical-microphone replay flow pending. |
| Webcam self-view | Author confirmed it works in the five-minute interview; video stays local. |
| Post-interview debrief | Verified live once on a fictional transcript. On the author's real run it hit Gemini HTTP 503 (provider overload); transient errors are now retried automatically. |
| Recorded-answer review, tailored questions and follow-ups | Verified live with synthetic and fictional input. Gemini text generation was re-verified on Oct 22 with a fictional brief. |
| Company research (Google Search grounding) | **Not verified live.** It repeatedly returned HTTP 429 on this key, and we did not retry in a loop. |
| Alexa+ itself | Not testable by entrants. This is a simulation plus a self-hosted MCP server. |

## Challenges

- **Turning a practice tool into an interview.** Early versions coached after every answer. Real interviews don't, so we moved all feedback to the end and built a focused room with nothing to click.
- **Streaming audio both ways in a browser.** That meant AudioWorklet resampling to 16 kHz, playing Maya's audio without gaps, stopping queued audio when the candidate interrupts, and cleaning up the microphone on every exit path.
- **Trustworthy feedback.** Model feedback can sound confident and still be wrong. Every quote is checked against the actual transcript, the deterministic checks never invent evidence, and the UI labels authored, rule-based and model-generated content differently.
- **Quota and provider limits.** An early OpenAI key had no quota, so the deterministic loop was designed to work with no model at all. Later, Gemini text calls briefly returned 503, and Search grounding returned 429. We stopped instead of retrying in loops.
- **MCP errors became HTTP 500.** See friction entry 1.

## Accomplishments

- A hands-free, timed mock interview with real follow-ups and feedback only at the end.
- Feedback that points at the exact phrase to change, with an honest comparison showing whether the retry changed it.
- A real MCP server (2025-11-25) that an assistant could drive with the same loop, including context across sessions that never stores what the candidate said.

## What we learned

- Useful interview feedback is mostly about specificity. Pointing at "we worked on the database" teaches more than any score.
- Realism matters more than features. Removing per-answer coaching made the practice feel like an interview.
- Agent-facing tools need instructions and honest annotations, not just function signatures.

## What's next

- Run and tune full 15- and 30-minute sessions with real candidates, including non-native speakers, before claiming impact.
- Connect the MCP tools to Alexa+ when developer access is available, so the debrief and retry loop can run by voice.
- Add more interview types (technical walk-throughs, system design) and trends in history over time.

## Product feedback (required)

### Gemini API: Live API and `generateContent`

- **Used for:**
  - the hands-free voice interview (Live API, with automatic turn detection, native audio, input and output transcription, context compression and session resumption);
  - the post-interview debrief, recorded-answer review, tailored questions and follow-ups, and text coaching (`generateContent` with JSON schemas);
  - company research (Google Search grounding).
- **What worked well:**
  - One server-side key covers voice, audio understanding and text.
  - Structured JSON output made the UI and quote filtering straightforward.
  - The Live API's automatic turn detection and native audio are what make the interview feel real.
- **What needs work:**
  - Search grounding returned HTTP 429 on our key, and text briefly returned 503, which makes live verification unpredictable before a deadline.
  - Long sessions need careful handling of GoAway and resumption.
- **Onboarding:** a key in a local `.env`. The Live API needed its own WebSocket bridge and careful audio format handling: 16 kHz in, 24 kHz out.
- **Would we build with it again?** Yes, especially for real-time voice practice.

### Model Context Protocol — specification and Python SDK (`mcp` 1.30.0)

- **Used for:** the self-hosted coaching server (FastMCP, Streamable HTTP, stateless, JSON responses) and the client inside our own web backend.
- **What worked well:**
  - A decorated Python function becomes a typed tool quickly.
  - Streamable HTTP mounted cleanly into FastAPI.
  - Protocol 2025-11-25 negotiated with no extra configuration.
  - `instructions`, tool `title` and `ToolAnnotations` were easy to add.
- **What needs work:**
  - Error handling across the client boundary (friction entries 1 and 2).
  - There is no app `version` parameter (entry 3).
  - Structured output with a bare `-> dict` return annotation (entry 6).
- **Onboarding:** reaching a working tool call took one short server plus the SDK client example.
- **Would we build with it again?** Yes. It gives one well-defined surface that both our web app and a voice assistant can call.

### Alexa+ (track)

- **Used for:** the target platform. We built the self-hosted MCP server path and a simulated Alexa+-style voice experience.
- **What worked well:** the rules allow a self-hosted MCP server or a simulation, so we could build without hardware.
- **What needs work:** entrants cannot connect a local MCP server to Alexa+ itself, so we could not test real Alexa voice turns with our tools (entry 4).
- **Onboarding:** Alexa+ preview access isn't available to entrants, so we started from the track's pointer to the MCP getting-started docs and built the self-hosted MCP server path directly. Getting a working local MCP tool call with the official Python SDK was straightforward. The missing piece was any way to hear our tools inside an actual Alexa+ conversation.
- **Would we build with it again?** Yes, if an Alexa+ test harness becomes available. Practice by voice is exactly the interaction this product needs.

### Browser APIs (Chrome): AudioWorklet, MediaRecorder, Web Audio, Speech Synthesis

- **What worked well:** low-latency microphone capture and playback entirely in the page.
- **What needs work:**
  - Chrome's MediaRecorder WebM files report `duration = Infinity` (entry 5).
  - Speech-synthesis voices vary by operating system.

## Friction log (optional; up to a 10% bonus)

Every entry below was observed during this build.

1. **Exceptions inside the MCP client context arrive as `ExceptionGroup`**
   - **Task:** return a tool's error message from our web endpoint.
   - **Steps:** called `ClientSession.call_tool` inside `streamable_http_client(...)` and `ClientSession(...)`, then raised `ValueError(result.content[0].text)` when `isError` was true.
   - **Expected:** our `ValueError` handler returns HTTP 400 with the message.
   - **Actual:** the exception left the async context wrapped in an `ExceptionGroup`, so FastAPI returned HTTP 500 "Internal Server Error" for every tool error.
   - **Severity:** Medium.
   - **Workaround:** keep the result, exit both contexts, then raise.
   - **Suggestion:** document this in the client quickstart, or unwrap single-exception groups.
2. **Tool errors are plain text with a fixed prefix**
   - **Actual:** the text reads `"Error executing tool compare_answer_texts: <message>"`.
   - **Severity:** Low.
   - **Workaround:** strip the prefix with a regular expression.
   - **Suggestion:** a structured error field, with a code and a message.
3. **No server version setting in FastMCP**
   - **Actual:** `initialize` reports `serverInfo.version = '1.30.0'`, the SDK's version, and `FastMCP.__init__` has no `version` parameter.
   - **Severity:** Low.
   - **Suggestion:** add a `version` argument.
4. **No way to test a local MCP server with Alexa+**
   - **Actual:** Alexa+ access is not available to entrants.
   - **Severity:** High for this track.
   - **Workaround:** a simulated experience plus MCP integration tests.
   - **Suggestion:** a public Alexa+ simulator that can connect to a developer's Streamable HTTP MCP endpoint.
5. **MediaRecorder WebM duration is Infinity in Chrome**
   - **Actual:** `audio.duration === Infinity` after `loadedmetadata`.
   - **Severity:** Low.
   - **Workaround:** seek to a very large time once, then back to 0.
6. **FastMCP silently omits `structuredContent` for `-> dict`**
   - **Actual:** with a bare `-> dict` return, the tool returned text only. Adding `structured_output=True` raised `InvalidSignature: return type <class 'dict'> is not serializable for structured output`.
   - **Severity:** Low to Medium; MCP Apps views depend on `structuredContent`.
   - **Workaround:** use `-> dict[str, Any]` with `structured_output=True`.
   - **Suggestion:** accept a bare `dict`, or warn.
7. **No reference host for testing MCP Apps views locally**
   - **Actual:** no MCP Apps-capable host was available to us.
   - **Severity:** Medium.
   - **Workaround:** we wrote `/mcp-app-preview`.
   - **Suggestion:** an official browser-based MCP Apps inspector.

## Feature requests (optional)

- **Alexa+ developer test console for self-hosted MCP servers.** Priority: Critical.
- **Structured tool errors in the MCP Python SDK.** Priority: Important.
- **Browser-based MCP Apps test host or inspector.** Priority: Important.
- **`version` argument for FastMCP.** Priority: Nice-to-have.

## What was built during the submission period

All of Rehearsal (`interview/`) was created during the submission period, in October 2026. The `trace/` folder is a separate, earlier experiment from the same week and is not part of this submission.
