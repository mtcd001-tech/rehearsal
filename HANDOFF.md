# Start here: Rehearsal agent handoff

Last updated: **October 22, 2026** (user timezone: America/New_York).

## Objective and user expectations

Build a compelling Amazon Developer Hackathon submission. The active idea is **Rehearsal**, an interview-practice app: a person-like interviewer asks tailored questions, listens to spoken answers, gives specific evidence-based coaching, and helps the user retry. The intended initial audience is technical-internship candidates, including non-native English speakers. Broader interview types are a future direction, not implemented coverage.

The user is busy and expects the agent to do most implementation and preparation. They liked Rehearsal's appearance and said to keep going. They now explicitly require a durable handoff and ongoing work log so another agent can continue. Follow `AGENTS.md` on every turn.

## Active decision / constraints

- **Rehearsal in `interview/` is active.** Root-level Trace is a paused earlier code-visualizer prototype; preserve it.
- User chose: **“Build the sample flow first; I’ll handle API access later.”** Do not keep retrying paid requests or block independent progress on API access.
- Sample and local rehearsal must be labeled honestly. No canned output represented as live AI; no fabricated scores, transcripts, measurements, experience, or feedback evidence.
- User values animation and a convincing experience, not just static screens. The interviewer is currently a custom animated SVG illustration, not photorealistic video.
- No need to ask permission repeatedly for ordinary implementation/testing. Do not claim the app or hackathon submission is complete when required external steps remain.

## Hackathon essentials previously verified

- Event: Build, Ship, Shape: Amazon Developer Hackathon.
- Deadline: **October 23, 2026, 3:00 p.m. EDT / noon PDT**. Target an earlier submission buffer.
- Proposed track: **Alexa+ simulated experience**, backed by actual MCP tools. Private Alexa+ preview access is unavailable to entrants; physical hardware and public app hosting are not required for this path.
- MCP requirement: specification 2025-11-25 or later, Streamable HTTP. Local handshake verified at 2025-11-25.
- Submission needs GitHub source/run instructions, public YouTube/Vimeo demo under 3 minutes, project description, and honest tool feedback. Public GitHub requires an open-source license; private access has named-reviewer requirements.
- No AWS credits available; no mini challenge eligibility claimed.
- Organizer update instructs freezing submitted code/video/materials after deadline until winners are announced (expected December 3).
- Verify current official rules again before final submission, especially if an agent resumes later.

Sources:
- https://amazonappdev2026.devpost.com/rules
- https://amazonappdev2026.devpost.com/details/faqs
- https://amazonappdev2026.devpost.com/resources
- https://amazonappdev2026.devpost.com/updates/46539-final-stretch

## Workspace and launch

- Windows PowerShell; workspace `D:\hackamazon`.
- Existing Python 3.11 virtual environment: `D:\hackamazon\.venv`.
- Node available (v22.23.1 observed).
- Git initialized, but **all project files remain untracked; no commits or remote publication are established** as of this handoff. Do not assume Git provides a backup.
- Start Rehearsal from workspace root:

```powershell
.venv\Scripts\python interview\server.py
```

- Open `http://127.0.0.1:8766`.
- Alternative: `interview/start.ps1`.
- Server may have been started manually by the user. Agent-owned server was stopped after prior tests. Check port/process state before starting another instance; do not terminate unrelated processes.
- Trace runs separately with root `server.py` on port 8765. Do not confuse the two servers or their similarly named test modules.

## Implemented Rehearsal behavior

### 1. Authored sample experience

- Warm cream/orange interface, illustrated seated interviewer (Maya), blinking/breathing/speaking animations, transcript panel, question card, sample timer.
- Browser speech synthesis narrates the original sample question, first answer, follow-up, and improved retry. Skip narration is available.
- Flow: Experience the sample → Play sample answer → See the coaching → Try that answer again → Play improved answer.
- Coaching cites sample phrases; separates structure, language, and technical depth. Retry comparison shows exact before/after text. JSON practice notes can be downloaded.
- Sample always uses fictional authored context, even if the user edits the brief. Labels disclose it is not a live AI interview.

### 2. Local microphone rehearsal (latest feature)

- Entry: **Practice my own answer**.
- Five original behavioral questions (ownership, tradeoffs, learning, collaboration, setbacks).
- Browser MediaRecorder captures microphone audio locally, with Web Audio activity meter and timer. Automatic stop at two minutes; maximum four takes per session.
- Each take has playback, manual transcript/notes field, word count of those notes, and audio download. User sets a retry focus and uses self-review prompts; notes export as JSON.
- **No upload, automatic transcription, or AI evaluation in this mode.** Browser speech synthesis can optionally read the question.
- Reset/switching modes/closing tab discards undownloaded recordings. Microphone tracks and object URLs are cleaned up. Delayed permission after reset is handled.

### 3. Live API paths implemented but not verified end to end

- FastAPI local server, OpenAI Realtime WebRTC setup, server-created ephemeral client secret, AI-generated audio output, microphone input/transcript events, typed AI practice.
- Editable brief: role, team/company, experience, job description.
- Explicit live-mode data-use dialog before connecting microphone. Standard API key stays on server. Browser gets a short-lived secret. Live sessions stop after ten minutes.
- MCP tools: `get_interview_brief`, `coach_latest_answer`, `compare_retry`.
- Browser gateway calls actual local MCP Streamable HTTP endpoint; Realtime function tools bridge to it.
- Model coaching/comparison quotes are filtered against actual answer text. Baseline/focus are stored for retry. No accent/personality/employability scores.
- Session state is in memory, cleaned roughly two hours after creation (30-second interval), on reset, or server exit. Host/Origin restrictions and loopback bind; not a public multi-user service.

## File map

| Path | Role |
|---|---|
| `AGENTS.md` | Mandatory continuity workflow |
| `HANDOFF.md` | This current-state snapshot |
| `WORK_LOG.md` | Append-only milestone history |
| `interview/README.md` | Setup, capabilities, limits, verification |
| `interview/server.py` | FastAPI endpoints, MCP tools, model requests, session management |
| `interview/sample.py` | Original sample brief, answers, coaching, comparison |
| `interview/static/index.html` | Practice room, SVG interviewer, dialogs, local recording panel |
| `interview/static/style.css` | Responsive visual design and animations |
| `interview/static/app.js` | Sample flow, speech, live WebRTC, transcript, coaching, reset |
| `interview/static/practice.js` | Local microphone rehearsal; no network calls |
| `interview/test_interview.py` | Backend/model-mock and local HTTP/MCP tests |
| `interview/test_practice.cjs` | Pure JS recording lifecycle tests using mocked browser APIs |
| `interview/.env.example` | Placeholder configuration; never put real secrets here |
| `interview/requirements.txt`, `start.ps1` | Dependencies and launch helper |
| Root `README.md`, `SUBMISSION.md`, `DEMO.md`, `trace-submission.zip` | **Old Trace materials, not valid Rehearsal submission assets** |

## Verification already performed

From `D:\hackamazon\interview`, with Rehearsal server running for integration tests:

```powershell
..\.venv\Scripts\python -m unittest test_interview -v
node test_practice.cjs
node --check static/app.js
node --check static/practice.js
```

- **8 Python tests passed** before latest frontend-only local recording addition: exact evidence filtering, retry prerequisites, empty-answer handling, deduplication, provider failure handling, malformed report rejection, session deletion, HTTP/MCP integration. Model responses are mocked; local HTTP/MCP calls are real.
- **JS recording lifecycle tests passed** after latest addition: record/stop saves take, reset cleanup, late permission releases tracks, permission denial recovers.
- JS syntax checks passed for both files.
- Earlier static check found no missing/duplicate literal DOM IDs before local recording addition; repeat if relevant after new HTML changes.
- **Real-browser QA done 2026-10-22 via Claude in Chrome** (desktop Chrome, Windows): full sample flow incl. speech/skip, coaching, retry, comparison, reset/restart; no console errors; no duplicate IDs; 390px mobile layout (iframe) has no horizontal overflow. Fixed three `?`-corrupted labels and sample-mode button-state bugs (see WORK_LOG). Re-ran Python 8/8 and JS tests after fixes.
- **Still unverified:** physical microphone record/playback/download (Record not clicked — permission prompt blocks automation), file-download clicks, real mobile device, live/text AI paths.

## API blocker and configuration

- An inherited `OPENAI_API_KEY` was present; no value was exposed or written to files.
- Minimal text request returned **429 `insufficient_quota`**. Realtime client-secret request returned **500 `server_error`**. Do not assume the latter is definitively a billing error.
- User explicitly deferred resolving API access. No provider requests were made after that choice.
- Future working key should be set locally in `interview/.env`, excluded by root `.gitignore`, or environment. `load_dotenv(..., override=True)` allows that file to override the inherited key.
- Default models: `gpt-4.1-mini` text; `gpt-realtime` voice. Verify current availability/docs when enabling.
- Configuration presence is not proof of working quota or voice access.

## Next priorities

1. Sample flow and layout are browser-verified. Remaining manual check: user records a take in **Practice my own answer** (record/stop/playback/retry/download, permission denial). Chrome automation is allowed without prompts via gitignored `.claude/settings.local.json`; avoid clicking Record/downloads through automation.
2. Keep the intended product centered on natural voice interviews and evidence-based retry coaching. Local recording is a useful interim feature, not a substitute for the unverified live AI goal.
3. Once user explicitly resolves API access: verify a real short voice conversation, transcription timing, tool calls after completed candidate turns, generated follow-ups, baseline/retry comparison, interruption, disconnect/error recovery, and costs. Do not invent successful integration.
4. Strengthen differentiation. Yoodli already provides interview roleplay and feedback; a realistic avatar alone is not original. Intended focus is transparent coaching and demonstrable retry improvement for internship communication. No customer validation yet.
5. Prepare **new Rehearsal** demo script, accurate submission copy, actual tool feedback/friction log, and GitHub repo. Do not reuse Trace descriptions. Public video and Devpost submission are not done.
6. Keep this file and the work log current after every milestone, per user request.

## Known risks / things to inspect

- Realtime input transcription may arrive after a model tool call. Current gateway waits for saves already queued but does not guarantee an unfinished transcription has arrived. Validate before claiming feedback always targets the latest spoken answer.
- Sample speech voices depend on browser/OS; unsupported speech falls back to readable text. Avatar animation is stylized, not true lip synchronization.
- Local audio capture is tested with mocks only. Codec support and physical device behavior need browser verification.
- Some shell output displayed mojibake when reading UTF-8 with PowerShell defaults. Inspect actual bytes/browser rendering before rewriting encodings; do not assume the files are corrupted from terminal display alone. Three labels with literal `?` corruption were fixed 2026-10-22; if new ones appear, grep for ` ? ` in static files.
- Frontend scripts are compact and share global state. Be careful with reset, in-flight narration, pending microphone permission, and switching between sample/local/live/text modes.
- No repository commits, deployment, public video, or hackathon submission yet.

## Current work state

No half-written implementation is intentionally pending. Latest completed work: first real-browser QA and sample-flow fixes (2026-10-22). Nothing is committed to git yet — recommend asking the user to approve a first commit and GitHub repo. The next agent should read the log, inspect current files/status, then continue the priorities above rather than restarting or rebuilding the app.
