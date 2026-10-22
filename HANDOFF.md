# Start here: Rehearsal agent handoff

Last updated: **October 22, 2026, overnight** (user timezone: America/New_York).

## Objective and user expectations

Build a compelling Amazon Developer Hackathon submission. The active project is **Rehearsal** (`interview/`): an interview-practice app where an illustrated interviewer asks behavioral questions, the candidate answers (voice recorded locally, or typed), and feedback quotes their exact words, names one priority, and compares the retry. Audience: technical-internship candidates, including non-native English speakers.

The user is busy and expects the agent to do most of the work. Overnight on Oct 22 they said: commit, write submission materials, and keep developing autonomously; they will review later. Follow `AGENTS.md` on every turn.

## Active decisions / constraints

- **Never credit Claude, Codex, or any AI as co-author** in commits, PRs, or docs (explicit user rule; also in `AGENTS.md`).
- Rehearsal in `interview/` is active. Trace was moved to `trace/` (paused; preserve it; not the submission).
- User chose "build the sample flow first; I'll handle API access later." **Do not make paid API calls.** The key had `429 insufficient_quota`; Realtime client-secret returned 500.
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
   - JSON export includes the checks. Audio never leaves the tab. The WebM Infinity-duration fix is in.
5. **MCP Apps view:** `interview/mcp_app/answer_check.html` is served as `ui://rehearsal/answer-check` (`text/html;profile=mcp-app`, prefersBorder). The check tools carry `_meta.ui.resourceUri` and `structured_output=True` (this needs `-> dict[str, Any]`). The reference host is at `/mcp-app-preview` (`static/mcp-app-host.html`). The spec was read from `modelcontextprotocol/ext-apps` `specification/draft/apps.mdx`. It has not been tried in a third-party host.
6. **Practice history:** `interview/history.py`; MCP `save_practice_result` and `get_practice_progress`; `/api/progress` GET/POST/DELETE; the file is `interview/data/practice_history.json` (gitignored); `INTERVIEW_HISTORY_FILE` overrides it.
7. **Optional captions:** `webkitSpeechRecognition`, opt-in checkbox `#live-captions`, Google disclosure, auto-restart while recording, late results land, user edits win, abort on reset. Mocked tests only; real speech results unverified.
8. **Live AI paths** (OpenAI Realtime WebRTC and typed AI practice): implemented, **unverified**, consent dialog.

## File map

| Path | Role |
|---|---|
| `README.md` | Rehearsal overview, setup, MCP usage, status table (judge-facing) |
| `SUBMISSION.md` | Devpost text draft, product feedback, friction log, feature requests; has **[fill in]** markers |
| `DEMO.md` | Timed demo script under 3 minutes and recording checklist |
| `AGENTS.md`, `HANDOFF.md`, `WORK_LOG.md` | Continuity protocol, this snapshot, history |
| `interview/server.py` | FastAPI and MCP server, endpoints, model calls, sessions |
| `interview/checks.py` | Deterministic answer checks |
| `interview/sample.py` | Authored sample scenario |
| `interview/static/index.html`, `style.css` | UI |
| `interview/static/app.js` | Sample flow, speech, live/text modes, coaching display |
| `interview/static/checks.js` | Rule-check renderer and API calls |
| `interview/static/practice.js` | Local practice: recording, typed takes, checks, compare |
| `interview/test_interview.py`, `test_checks.py`, `test_practice.cjs` | Tests |
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
- **Not verified:** physical microphone, real phone, file-download clicks, live AI paths, and new code on the user's 8766 server (it needs a restart).

## Next priorities

1. The user should restart their server, try the sample and Practice-my-own-answer with a real microphone, then review `README.md`, `SUBMISSION.md`, and `DEMO.md`.
2. User actions needed:
   - Create a public GitHub repo and push. Ensure the MIT license shows in About.
   - Record and upload the demo.
   - Fill in the **[fill in]** markers.
   - Submit on Devpost before **Oct 23, 12:00 p.m. PT**.
3. Optional improvements, if time remains:
   - Try the MCP App in a real MCP Apps host if the user has one.
4. Never claim live AI works until it is verified with a working key and the user allows paid calls.

## Known risks

- Rule checks use English word lists. They can misfire ("profiled" counts as verification) and will miss paraphrases. They are presented as prompts, not judgments.
- Realtime transcription may arrive after a tool call (live path; unverified).
- Speech voices vary by operating system. The avatar is stylized, with no lip sync.
- Frontend scripts share global state (`mode`, `generation`, `phase`). Be careful with reset and in-flight async work; generation and requestVersion guards are used.
- PowerShell may display UTF-8 as mojibake. Check the actual bytes before "fixing" the encoding.

## Current work state

Everything described above is committed on `main` (see `git log`). There is no remote. If an agent resumes: read the latest `WORK_LOG.md` entries, run the tests, then continue with Next priorities item 3, or help the user with item 2.
