> **Continuing agent:** Read [HANDOFF.md](../HANDOFF.md), [AGENTS.md](../AGENTS.md), and [WORK_LOG.md](../WORK_LOG.md) before editing. Update the handoff and log after each meaningful milestone.

# Rehearsal — interview practice

A practice room for behavioral interviews: an illustrated interviewer, spoken questions, feedback tied to your exact words, one priority to fix, and a retry comparison. The coaching engine is a self-hosted MCP server whose core tools are deterministic and need no API key. The repository overview is in the [root README](../README.md); the paused Trace prototype now lives in `../trace/`.

## Try it now

From D:\hackamazon:

```powershell
.venv\Scripts\python interview\server.py
```

Open **http://127.0.0.1:8766**. Click **Experience the sample**, then **Play sample answer**, **See the coaching**, **Try that answer again**, and **Play improved answer**. The coaching and comparison each include a panel computed live by the `check_answer_text` / `compare_answer_texts` MCP tools on the sample text. Skip narration advances the current spoken segment. Download practice notes exports only the displayed session as JSON.

Alternatively run `interview/start.ps1` from PowerShell. For a fresh checkout: create a Python 3.11+ virtual environment, install this directory's `requirements.txt`, then run `server.py`.

## What sample mode does

- Plays an original, authored engineering-internship scenario using browser speech synthesis when supported.
- Displays an original SVG interviewer with breathing, blinking, and speaking animation. This is an illustration, not generated human video or photorealistic lip sync.
- Shows a first answer, an interviewer follow-up, feedback tied to exact phrases, and a clearer retry.
- Separates structure, language clarity, and technical depth.
- Keeps the sample in browser memory. No microphone or model API is used in this mode. The rule-check panels send the authored sample text to the local server only. Browser voice availability varies; text remains readable if speech fails. Some OS/browser voices may use their own online speech service.
- The sample always uses its own fictional context. Editing Your brief affects subsequent live/text sessions, not the authored sample.

## Live implementation and current blocker

The app includes WebRTC Realtime voice, a server-side ephemeral-token endpoint, typed AI practice, and MCP tools for context, coaching, and retry comparison. **These AI paths are not verified end to end.** The configured API credential returned `429 insufficient_quota` for a minimal text request, and Realtime token setup returned HTTP 500. Work on provider access was deferred at the user's request. No further provider calls were made after that decision.

When ready, copy `.env.example` to `.env` in this directory and set a working key locally. Do not put it in a chat, browser source, screenshot, or Git commit. Restart the server. Explicit values in `.env` override inherited environment values.

Click Start live interview to read the data-use explanation and opt into microphone access. The standard API key stays on the server; the browser receives a short-lived client secret. Live sessions stop after ten minutes. End conversation closes the WebRTC connection and microphone tracks. Reset clears this app's in-memory session. This does not erase provider-side records.

Live voice sends audio and context to OpenAI; text practice and coaching send the brief and transcript. Raw audio is not stored by this app. Live session state is in server memory, cleaned approximately two hours after creation (30-second cleanup interval), on Reset, or at server shutdown. The local service is single-user, loopback-only, and not prepared for public hosting. No analytics or webcam capture is included.

## MCP and hackathon positioning

Streamable HTTP endpoint: **http://127.0.0.1:8766/mcp**

Tools (the server also publishes agent instructions describing the practice loop, plus titles and read-only annotations):

- `check_answer_text(answer, question?)` — deterministic wording checks with exact quotes and one priority. No key needed.
- `compare_answer_texts(before, after)` — deterministic per-signal change between two takes, with before/after quotes. No key needed.
- Both check tools link to the MCP Apps view `ui://rehearsal/answer-check` (`mcp_app/answer_check.html`) and return `structuredContent`. `/mcp-app-preview` is a minimal local reference host for it (sandboxed iframe, postMessage JSON-RPC, message log); `/api/app-resource` and `/api/app-call` back that page through the real MCP endpoint.
- `get_practice_progress()` / `save_practice_result(question, first_answer, retry_answer?)` — opt-in local history of signal labels and counts (never answer text or audio) so an agent can start a session with context. Deleting history is an app action (`DELETE /api/progress`), deliberately not an MCP tool.
- `get_interview_brief(session_id)` — retrieve the supplied context and recorded transcript.
- `coach_latest_answer(session_id)` — call the model, verify quoted evidence exists in the actual answer, attach the rule checks, store the baseline and retry focus.
- `compare_retry(session_id)` — compare a new answer with the coached baseline and filter unsupported quotes.

The web endpoints `/api/tool`, `/api/check`, and `/api/compare-text` invoke the real MCP endpoint through the SDK's Streamable HTTP client. Realtime function calls are bridged through the same gateway. Protocol **2025-11-25** was verified locally. Coaching model calls were tested with mocks, not a functioning paid API.

This is an **Alexa+ experience simulation**, not an Alexa device integration. The sample alone is not a competitive demonstration of the live integration; validate an actual AI interview before submitting.

## Boundaries

This is practice feedback, not a hiring decision, clinical assessment, or validated skill score. No numeric confidence, personality, accent, or employability scores are produced. Transcript-only feedback cannot assess pronunciation or audio fluency. The coach is instructed not to invent experience or performance metrics. Quote filtering prevents invented evidence snippets but does not guarantee that all generated advice is correct.

Prior art: [Yoodli](https://yoodli.ai/use-cases/interview-preparation) already provides interview roleplay and feedback. Rehearsal does not claim that category as novel. The intended focus is a transparent, evidence-based retry loop for technical internship communication; distinctiveness and learner impact remain to be validated.

## Verification

Keep the server running, then from this directory:

```powershell
..\.venv\Scripts\python -m unittest test_interview test_checks test_history -v
node test_practice.cjs
```

Set `INTERVIEW_PORT` when the server under test runs on another port. For UI testing of the AI paths without paid calls, `INTERVIEW_PROVIDER_BASE_URL` can point the server at a local mock chat-completions endpoint (leave it unset in normal use; it defaults to `https://api.openai.com/v1`). Anything produced that way is mock output and must not be presented as AI feedback. 24 Python tests cover practice history (no text stored, recurring focus, corrupt-file handling, clear), the rule checks (exact-substring quotes, no score fields, honest unchanged-retry wording), evidence quote filtering, retry requirements, empty answers, transcript deduplication, provider failures, schema checks, session deletion, and HTTP plus real MCP integration (tool list, instructions, annotations, error responses). No provider request is made.

Browser QA (October 22, 2026, desktop Chrome on Windows): the full sample flow, browser speech with skip, coaching, retry comparison, and reset/restart were exercised with no console errors, and a 390px-wide layout showed no horizontal overflow. Physical microphone recording, file downloads, real mobile devices, and the live AI paths have not been verified.

## Sources used for implementation

- https://developers.openai.com/api/docs/guides/voice-webrtc
- https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create
- https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create

## Still required before hackathon submission

Public GitHub repository, demo video (script in `../DEMO.md`), and final review of `../SUBMISSION.md` by the author. Live voice/AI validation needs working API access; until then the submission presents the deterministic MCP tools, local practice, and the authored sample, and labels the live path as unverified. Learner impact is not validated.

## Local practice (no API key)

Choose **Practice my own answer**. Pick one of ten original behavioral questions (ownership, tradeoffs, learning, collaboration, setbacks, debugging, explaining a project, feedback, deadlines, ambiguity), optionally hear it, then **Record my answer** (microphone) or **No microphone? Type an answer**. Recording shows an activity meter and timer and stops automatically at two minutes; up to four takes are kept in the tab.

For each take, write or paste what you said and press **Check my words**. The text (not the audio) is sent to this app's local server, which runs the deterministic `check_answer_text` MCP tool and shows quoted findings and one priority. After a second take with text, **Compare first and latest take** runs `compare_answer_texts`. Download practice notes exports your text, focus, check results, and comparison as JSON; recordings download separately.

Optional: tick **Draft a transcript while I speak** before recording to have the browser's speech recognition fill the take's transcript (it keeps updating briefly after you stop, and never overwrites your own edits). In Chrome, this sends audio to Google's speech service, so it is off by default and disclosed next to the checkbox. It is hidden when the browser has no speech recognition. Real recognition results have not been verified by the agent (headless Chrome returned none); logic is covered by mocked tests.

Without that option, audio is never uploaded and is not transcribed automatically. Reset, switching modes, or closing the tab discards undownloaded takes. Microphone tracks are released on stop, reset, and leaving the page.

Local recording logic tests: `node test_practice.cjs` (mocked browser APIs: capture/stop, cleanup, delayed permission, permission denial, typed takes, check gating, comparison arguments, stale results after reset, take limit). In headless Chrome with Chrome's fake microphone device, a real MediaRecorder take was recorded, played (duration fixed from Chrome's WebM `Infinity`), checked, compared, and reset. A physical microphone has not been tested by the agent.

## Resume upload

Open **Your brief** or **Edit brief**, then choose a PDF, DOCX, or UTF-8 TXT resume (up to 5 MB). Extraction runs locally in memory with a 10-second worker timeout; original files are not stored. Review/edit the extracted text, click **Use this text in Your experience**, then **Save interview brief**. Apply replaces the draft experience field; selecting a file alone does not overwrite it. Closing the dialog discards an unapplied import.

PDFs must contain selectable text and be unlocked (maximum 15 pages); scanned PDFs need OCR elsewhere first. Legacy `.doc` files are not supported. Imports are limited to 10,000 characters with a visible truncation notice. Complex columns/tables may extract in the wrong order, so review before saving. The authored sample and local rule checks do not personalize themselves from this resume; the saved brief is context for subsequent live/text AI sessions when API access is enabled. Those sessions send the brief to the configured provider as disclosed in the app.

After updating an existing checkout, install updated dependencies and restart the server:

```powershell
.venv\Scripts\python -m pip install -r interview/requirements.txt
.venv\Scripts\python interview/server.py
```

Tests: from `interview/`, run `..\.venv\Scripts\python -m unittest test_resume -v` and `node test_resume.cjs`. Seven Python tests exercise extraction and the real subprocess endpoint, including bad inputs; JS mocks check preview/apply/stale-request behavior. Browser file-picker testing is still pending.
