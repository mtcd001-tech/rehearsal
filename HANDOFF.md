# Start here: Rehearsal agent handoff

Last updated: **October 22, 2026, Gemini tailored-question milestone** (user timezone: America/New_York).

## Objective and user expectations

Build a compelling Amazon Developer Hackathon submission. The active project is **Rehearsal** (`interview/`): an interview-practice app where an illustrated interviewer asks behavioral questions, the candidate answers (voice recorded locally, or typed), and feedback quotes their exact words, names one priority, and compares the retry. Audience: technical-internship candidates, including non-native English speakers.

The user is busy and expects the agent to do most of the work. Overnight on Oct 22 they said: commit, write submission materials, and keep developing autonomously; they will review later. Follow `AGENTS.md` on every turn.

## Active decisions / constraints

- **Never credit Claude, Codex, or any AI as co-author** in commits, PRs, or docs (explicit user rule; also in `AGENTS.md`).
- Rehearsal in `interview/` is active. Trace was moved to `trace/` (paused; preserve it; not the submission).
- User chose "build the sample flow first; I'll handle API access later." **OpenAI calls remain deferred. On Oct 22 the user supplied a Gemini key locally and explicitly authorized Gemini implementation/testing.** The key had `429 insufficient_quota`; Realtime client-secret returned 500.
- Honesty: authored sample content is labelled as authored; rule checks are labelled deterministic/no AI; the live AI path is labelled unverified. No fabricated scores, transcripts, metrics, or feedback evidence.
- Publishing (GitHub repo creation/push, YouTube upload, Devpost submission) is outward-facing: **the user must do it or explicitly approve it.** No remote exists yet.
- Ordinary implementation and testing do not need repeated permission.

## Hackathon essentials (re-verified Oct 22 from the official rules page)

- Deadline **Fri Oct 23, 2026, 12:00 p.m. PT / 3:00 p.m. ET**.
- Track: **Alexa+**. Either a self-hosted MCP server (spec ≥ 2025-11-25, Streamable HTTP), or a simulated Alexa+ experience. Rehearsal qualifies on both.
- Required:
  - GitHub repo with setup instructions. Public repos need a detectable open-source license (MIT is present).
  - Text description.
  - Public YouTube/Vimeo demo under 3 minutes.
  - Product feedback per tool: what it was used for, what worked, what needs work, onboarding, would you build again.
  - Track selection.
- Optional friction log (task, steps, expected vs. actual, severity, workaround, suggestion) earns **up to a 10% bonus**. Optional feature requests (with a priority).
- Judging criteria, equally weighted:
  - Tech implementation.
  - Design.
  - Potential impact.
  - Quality of idea. "Basic MCP wrapper" is called obvious; "context-aware add-on that maintains state across sessions", "MCP Apps", and media cards are called creative.
- Freeze submitted materials after the deadline until winners are announced (~Dec 3).
- Sources: https://amazonappdev2026.devpost.com/rules (WebFetch got 403; curl with a browser user agent worked), `/details/faqs`, `/resources`.

## Workspace and launch

- Windows; workspace `D:\hackamazon`; venv `D:\hackamazon\.venv` (Python 3.11.9; packages match `interview/requirements.txt`). Node v22.
- Run: `.venv\Scripts\python interview\server.py` → http://127.0.0.1:8766 (or `interview/start.ps1`). `INTERVIEW_PORT` changes the port.
- **The user's own server process on 8766** was started before the overnight work, so it is running **old code** until restarted. Do not kill it without reason. The agent used its own server on **8767** for testing.
- Tests (server must be running; set `INTERVIEW_PORT` to match):
  - `cd interview; ..\.venv\Scripts\python -m unittest test_interview test_checks -v`
  - `node test_practice.cjs`
- Headless browser QA: the Claude-in-Chrome extension disconnected overnight. The agent used a CDP driver in its session scratchpad (not in the repo): headless Chrome with `--use-fake-ui-for-media-stream --use-fake-device-for-media-stream`.

## Implemented behavior

1. **Authored sample:** animated SVG interviewer (Maya), browser speech with skip, transcript, coaching tabs, retry, before/after comparison, JSON download. The coaching and comparison sections also show **live panels computed by the MCP tools** on the sample text.
2. **Deterministic rule checks** (`interview/checks.py`):
   - Signals: ownership (I vs we, and I+action), concrete actions, verification, vague outcomes, fillers (text only), numeric claims to support, reflection or limits, length.
   - Quotes are exact substrings. One priority is chosen. Compare reports per-signal count direction, honestly.
   - No scores.
3. **MCP server** (FastMCP, stateless Streamable HTTP, protocol 2025-11-25):
   - Tools: `check_answer_text`, `compare_answer_texts` (no key); `get_interview_brief`; `coach_latest_answer` and `compare_retry` (need a key; quote-filtered; coach also attaches rule checks).
   - Server `instructions` describe the coaching loop for agents. Tools have titles and annotations (the check tools are read-only and idempotent).
   - Web endpoints `/api/tool`, `/api/check`, `/api/compare-text` call the real MCP endpoint via the SDK client. Tool errors now return 400 with a readable message (previously 500).
4. **Local practice:**
   - Record (MediaRecorder, meter, 2-minute cap, 4 takes) or type a take. Per-take **Check my words**; **Compare first and latest take**.
   - JSON export includes the checks. Audio stays local unless Gemini review or browser captions is explicitly selected. The WebM Infinity-duration fix is in.
5. **MCP Apps view:** `interview/mcp_app/answer_check.html` is served as `ui://rehearsal/answer-check` (`text/html;profile=mcp-app`, prefersBorder). The check tools carry `_meta.ui.resourceUri` and `structured_output=True` (this needs `-> dict[str, Any]`). The reference host is at `/mcp-app-preview` (`static/mcp-app-host.html`). The spec was read from `modelcontextprotocol/ext-apps` `specification/draft/apps.mdx`. It has not been tried in a third-party host.
6. **Practice history:** `interview/history.py`; MCP `save_practice_result` and `get_practice_progress`; `/api/progress` GET/POST/DELETE; the file is `interview/data/practice_history.json` (gitignored); `INTERVIEW_HISTORY_FILE` overrides it.
7. **Optional captions:** `webkitSpeechRecognition`, opt-in checkbox `#live-captions`, Google disclosure, auto-restart while recording, late results land, user edits win, abort on reset. Mocked tests only; real speech results unverified.
8. **Ten practice questions.** The 'I + action' rule accepts present tense and a lowercase 'i'. Maya can speak the tip aloud ('Hear Maya say the tip').
9. **`agent_sim.py`:** scripted assistant turn order with real tool calls. It is not an LLM.
10. **Live AI paths** (OpenAI Realtime WebRTC and typed AI practice): implemented, **unverified**, consent dialog.

## File map

| Path | Role |
|---|---|
| `README.md` | Rehearsal overview, setup, MCP usage, status table (judge-facing) |
| `SUBMISSION.md` | Devpost text draft, product feedback, friction log, feature requests; has **[fill in]** markers |
| `DEMO.md` | Timed demo script under 3 minutes and recording checklist |
| `AGENTS.md`, `HANDOFF.md`, `WORK_LOG.md` | Continuity protocol, this snapshot, history |
| `interview/server.py` | FastAPI and MCP server, endpoints, model calls, sessions |
| `interview/checks.py` | Deterministic answer checks |
| `interview/history.py` | Opt-in practice history (derived signals only) |
| `interview/agent_sim.py` | Scripted terminal agent running the loop over MCP (`--demo`, `--save`) |
| `interview/mcp_app/answer_check.html` | MCP Apps view (`ui://rehearsal/answer-check`) |
| `interview/static/mcp-app-host.html` | Local MCP Apps reference host at `/mcp-app-preview` |
| `docs/screenshots/` | Real captures for the Devpost gallery |
| `interview/sample.py` | Authored sample scenario |
| `interview/static/index.html`, `style.css` | UI |
| `interview/static/app.js` | Sample flow, speech, live/text modes, coaching display |
| `interview/static/checks.js` | Rule-check renderer and API calls |
| `interview/static/practice.js` | Local practice: recording, typed takes, checks, compare |
| `interview/test_interview.py`, `test_checks.py`, `test_history.py`, `test_practice.cjs` | Tests |
| `trace/` | Paused Trace prototype and its own old docs |

## Verification status

- **Python:** 24/24 OK against the agent's 8767 server (run with `INTERVIEW_HISTORY_FILE` pointing to a scratch file).
- **JS:** mocked tests PASS. `node --check` passes on all scripts.
- **Real Chrome (extension, earlier on Oct 22), desktop:** sample flow, speech/skip, reset/restart; no console errors.
- **Headless Chrome (overnight):**
  - Sample rule panels show real MCP output.
  - Local practice: recording with the **fake** microphone device, playback duration, check, typed take, compare, reset.
  - 390px viewport: no horizontal overflow.
  - Screenshots reviewed.
- **Final overnight regression** (early morning Oct 22), all passing: Python 24/24; JS mocked tests; headless sample, local practice, progress, MCP App, spoken tip, and 390px checks. The agent's test servers are stopped.
- **Not verified:** physical microphone, real phone, file-download clicks, live AI paths, and new code on the user's 8766 server (it needs a restart).

## Next priorities

The user-facing morning steps are in `docs/SUBMIT_CHECKLIST.md`. The GitHub CLI (`gh`) is not installed, so publishing goes through github.com plus `git push`.


1. The user should restart their server, try the sample and Practice-my-own-answer with a real microphone, then review `README.md`, `SUBMISSION.md`, and `DEMO.md`.
2. User actions needed:
   - Create a public GitHub repo and push. Ensure the MIT license shows in About.
   - Record and upload the demo.
   - Fill in the **[fill in]** markers.
   - Submit on Devpost before **Oct 23, 12:00 p.m. PT**.
3. Optional improvements, if time remains:
   - Try the MCP App in a real MCP Apps host if the user has one.
4. Never claim live AI works until it is verified with a working key and the user allows paid calls.

## Demo video fallback

- `demo-video/rehearsal-demo-captioned.avi` is git-ignored: 1:43, silent, captioned, MJPEG at 126 MB.
- Its structure has been validated, but it has never been played in a player.
- To regenerate it, use the scripts in the agent scratchpad (`make_video.mjs` with CAPTURE_ONLY=1, then `render_avi.mjs`). Those are session-local and may be gone; the approach is described in WORK_LOG.

## Known risks

- Rule checks use English word lists. They can misfire ("profiled" counts as verification) and will miss paraphrases. They are presented as prompts, not judgments.
- Realtime transcription may arrive after a tool call (live path; unverified).
- Speech voices vary by operating system. The avatar is stylized, with no lip sync.
- Frontend scripts share global state (`mode`, `generation`, `phase`). Be careful with reset and in-flight async work; generation and requestVersion guards are used.
- PowerShell may display UTF-8 as mojibake. Check the actual bytes before "fixing" the encoding.

## Latest milestone: resume upload

- User asked to inspect overnight work and add resume upload. Overnight additions were preserved; clean baseline was `a00a655`.
- Added `interview/resume_import.py`, `static/resume.js`, `test_resume.py`, `test_resume.cjs`; updated brief dialog, server endpoint `/api/resume`, requirements (`pypdf==6.21.2`) and READMEs.
- PDF/DOCX/TXT up to 5 MB, in-memory extraction in a 10-second subprocess; PDF up to 15 pages; max 10,000 extracted characters with truncation notice. Original file is never saved. No OCR, legacy DOC, or encrypted PDF support.
- Editable preview; explicit Apply replaces draft experience; Save commits the brief. Existing experience is preserved on selection/errors; closing dialog cancels/ignores stale extraction.
- Seven Python parser/ASGI endpoint tests passed with real subprocesses and synthetic fixtures; JS preview/apply/stale-result mocks passed; existing practice JS regression passed; JS syntax and git diff checks passed. No paid provider calls. New file-picker UI not browser-tested this turn.
- Existing servers need updated dependencies and restart. User server was not terminated.
- Continuity instruction strengthened: write IN PROGRESS checkpoint BEFORE editing, update after small batches, and reconcile incomplete entries against files on resume. No reliance on a final handoff message.
- Authorship rule remains in force: commits use user's configured identity, no tool co-author credits.

## Current work state

User clarified that company/JD/resume research should tailor the simulated interview, NOT suggest resume edits. Earlier resume-edit suggestions were replaced with `experience_probes`: exact resume/JD evidence, follow-up questions and listen-for criteria. The plan includes proposed format, sequence, difficulty and core questions. UI: **Build my tailored interview**. Apply saves the full plan (including deep dives) to draft research context; Save passes it to subsequent AI sessions. Text, voice and coaching prompts explicitly use this context and adapt to actual answers. The authored demo and local question bank remain fixed.

Files: `interview/research.py`, `static/research.js`, `server.py`, research tests and brief UI. `/api/research` remains OFF unless `INTERVIEW_RESEARCH_ENABLED=1`; do not enable or make paid calls while deferral remains. Company/role only go into web search; resume/JD enter subsequent synthesis. Exact quotes filter fabricated evidence, not all bad advice. Sources and inferred interview formats need review.

Verification for clarification: 8 research Python tests with mocked providers (including plan propagation to text interviewer), JS research/resume mocks and research JS syntax pass. Prior milestone: 22 checks/history/resume Python tests and practice JS mocks passed. New UI and actual provider search/quality are unverified. No server restarted, no paid calls, no remote created. Existing overnight integration/browser results do not cover these new controls.

Next: restart the local server, verify resume preview/apply and research controls in a browser (disabled state first); once the user resolves API access and lifts deferral, verify real cited research and synthesis. Continue submission priorities above. Do not redo overnight work.

## Latest UI milestone

Readability pass completed: larger type/contrast and controls throughout; **Interview setup** navigation; numbered sections for job, experience and interview plan; resume upload followed by editable experience; saved-plan text in expandable details; responsive setup fields and save footer. Existing element IDs and JS behavior retained. HTML nesting/unique IDs verified and research/resume/practice JS mocks passed. Browser inventory was empty, so visual/keyboard/mobile QA remains pending. No paid calls or server restart. Next agent should visually check this UI before claiming it is browser-verified.

## Latest addition: skills development goals

Optional `skills` brief field (max 1,000 chars), labeled **Skills I want to improve**, added to setup after experience. Save/reopen, research synthesis and text/voice/coaching context include it. Goals are treated as learning priorities, not claimed abilities; text alone cannot assess pronunciation/fluency. Skills changes invalidate the research plan. No change to fixed demo/local rule checks. Eight research Python mocks and JS research mocks pass; JS syntax passes. No paid calls, server restart or browser verification. Next: restart and check setup save/reopen; live behavior only after API deferral is lifted.

## Latest addition: interview round and length

Brief fields `round` (recruiter/behavioral/technical/hiring_manager) and `duration` (string 5/15/30) default to behavioral/15. Setup save/reopen and research invalidation include both. Research synthesis and interviewer/coaching prompts receive both. Voice browser timer disconnects at selected limit; text gives one reminder without discarding input; sample unaffected. Existing 10-minute UI cutoff replaced. Nine research Python mocks, research/practice JS mocks, syntax and new timer boundary mocks pass. No paid calls/server restart/browser or live voice verification. Next: restart, check selectors/save/reopen and live behavior after API deferral ends.

## Latest: user test pass
Demo no longer overwrites personal setup; summary shows round/duration and demo export uses fictional brief. Setup/timer/research/resume JS mocks pass. docs/USER_TEST.md contains the manual no-API checklist. Full reload clears page-memory setup. No browser QA or paid calls. Next: incorporate user test findings.

## Latest: answer improvement and voice failure recovery
User reported live HTTP 429 and requested answer assessment/improvement. Added AI coach improved_answer and missing_details output, labeled draft in coaching UI; original transcript/baseline unchanged. Local rule feedback includes a revision checklist (not AI rewriting). Failed live setup now resets question/state and offers local recovery, retaining setup; explicit 429 message. Tests: 17 Python CoachTests/checks PASS (mock provider), setup/practice/recovery JS mocks PASS and JS syntax PASS. No paid calls, browser rendering or actual AI rewrite quality verified. Next: user tests local checklist; real AI review needs working API access and lifting deferral.

## Current milestone: Gemini recorded-answer review

User authorized Gemini testing after saving key in gitignored interview/.env. Implemented audio_review.py, POST /api/audio-review (12 MB in-memory WAV, bounded context), static/audio-review.js (browser WAV conversion to mono 16kHz, consent, transcript + feedback + rewrite), and practice integration. Recording remains local until Analyze my recording with Gemini or the explicit Analyze after I stop checkbox is selected. Only audio/question/skill goals go to Google, not resume. Key stays server-side. Browser captions remain a separate option.

Default GEMINI_AUDIO_MODEL=gemini-3.5-flash. Live synthetic speech test SUCCESS: matching transcript, feedback, 3 valid evidence snippets. Earlier listed models returned 404/503. Draft contained an inference about a missing index, so prompt tightened; generated draft must still be checked. No personal user recording/resume sent. Test WAV is gitignored in interview/data/gemini-test.wav. Key never printed.

Tests: 4 audio Python tests plus 8 coach tests PASS (mocks), audio frontend mocks PASS (WAV/transcript/edit preservation/stale result), existing practice JS PASS, syntax PASS. Real browser microphone/conversion/rendering remains unverified. No user server restart. OpenAI live voice/text and company research still use OpenAI; Gemini recorded review is separate, not continuous Gemini Live conversation. Next: restart server and user tests Practice my own answer -> enable Gemini auto analysis -> Record -> Stop -> review -> retry. Continue adapting questions/company research to Gemini only as a subsequent task.

## Latest completed milestone: Gemini question -> recording -> follow-up

User said to keep working and will review later. Added shared gemini_json helper, gemini_questions.py, POST /api/practice-question and static/practice-questions.js. In recorded practice, Ask a question from my setup explicitly sends saved brief (including resume/JD if supplied). Generated question appears on stage; Hear the question reads it. Audio review includes Practice this answer again (restores question/focus) and Ask me a follow-up (uses corrected transcript if present). No web search is performed by Gemini question generation. OpenAI live button is now labeled OpenAI live voice.

Retry comparisons and history group the latest eligible take with other takes answering exactly the same question. New question requests ignore stale results after Reset, and cannot change questions during recording. Four-take limit still applies.

Verification: live fictional follow-up HTTP 200, grounded in benchmarking/index tradeoffs. FULL Python regression 47/47 PASS against an owned temporary loopback server with scratch history; real MCP calls included, providers mocked in regression. Temporary server stopped. Eight JS test files PASS; HTML balanced/unique IDs/scripts checked. Browser UI/real microphone/conversion remain unverified; prior live audio test was synthetic. No personal user data used in provider testing and no OpenAI calls.

README, interview README, SUBMISSION and DEMO updated to distinguish the working Gemini backend from no-key MCP tools and unverified OpenAI voice. Demo now has a Gemini route with explicit browser preflight. Next: user browser test on restarted app, fix findings; optionally migrate company research to Gemini later. Do not claim the model generates verified company questions or guarantees factual rewrites.
