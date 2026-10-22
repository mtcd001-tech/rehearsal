# Rehearsal work log

Append meaningful milestones here. Keep `HANDOFF.md` as the current snapshot. Dates use America/New_York. Earlier entries below are reconstructed from completed work and tool results; no exact clock times are claimed.

### 2026-10-22 — Hackathon research and initial Trace prototype
- Purpose: assess feasibility before October 23, 3 p.m. EDT deadline.
- Changes: researched official rules/FAQ/resources; built Trace at repository root with actual Python tracing, visual state, sample corrections, and MCP navigation. Added Trace README, submission draft, demo script, tests, and ZIP.
- Verification: seven Trace tests passed, including actual local MCP protocol 2025-11-25 handshake. Browser unavailable.
- Decision: Trace lacked strong Amazon fit and differentiation; paused after user proposed interview coaching. Preserve it; do not use its submission materials for Rehearsal.

### 2026-10-22 — Rehearsal sample and API architecture
- Purpose: test user's mock-interview concept with voice, an interviewer presence, and evidence-based coaching/retry.
- Changes: created `interview/` with FastAPI/MCP server, original sample scenario, animated SVG interviewer, speech synthesis, transcript, coaching tabs, retry comparison, editable brief, download, live WebRTC and typed AI paths, setup docs.
- Research: Yoodli already offers similar interview roleplay; novelty not established. Used official OpenAI WebRTC/client-secret/Chat Completions docs.
- Verification: eight Python tests passed; actual local MCP handshake/tool context worked at 2025-11-25. Coaching/comparison provider outputs tested with mocks. JS syntax and initial DOM-ID checks passed.
- Blocker: minimal real text call returned 429 insufficient_quota; Realtime token call returned 500 server_error. User chose sample-first and deferred API access. No further paid calls after this choice.
- Limitations: no browser/audio/WebRTC end-to-end QA available. Sample is explicitly authored, not live AI.

### 2026-10-22 — Local microphone rehearsal
- Purpose: let user practice their own answers while API access is deferred; user liked the sample and requested continued work.
- Changes: added `interview/static/practice.js`, local practice panel/styles, reset cleanup hook in `app.js`, `test_practice.cjs`, README instructions. Five curated questions, two-minute recording limit, activity meter, up to four takes, playback/audio download, manual notes/transcript, retry focus, notes export.
- Verification: `node test_practice.cjs` passed mocked recording/save, reset cleanup, late permission cleanup, and permission-denial recovery. `node --check static/app.js` and `node --check static/practice.js` passed.
- Limitations: no automatic transcription or AI evaluation; no audio uploads. Physical microphone and browser behavior unverified. Switching modes/reset discards undownloaded takes.
- Next action: browser/local recording QA if possible; continue improving the active Rehearsal project without paid API retries.

### 2026-10-22 — Persistent agent handoff established
- Purpose: user explicitly requested documentation sufficient for a brand-new agent and mandatory ongoing updates.
- Changes: added root `AGENTS.md` continuity instructions, detailed `HANDOFF.md` state snapshot, this `WORK_LOG.md`, and entry links in project READMEs.
- Verification: inspected workspace/file inventory and `git status`; all source remains untracked, no established commit/remote. Checked that handoff references match actual project paths.
- Limitations: documentation does not itself publish, back up, or complete the project. API and browser verification blockers remain as recorded above.
- Next action: read `HANDOFF.md` next-priority list, continue Rehearsal, append a milestone entry and refresh snapshot after meaningful changes.

### 2026-10-22 — First real-browser QA (Claude in Chrome) and sample-flow fixes
- Purpose: HANDOFF priority 1, browser verification. Chrome automation became available this session.
- Changes:
  - `interview/static/index.html`: fixed literal `?` corruption in three labels ("Skip narration →", "LOCAL RECORDING · NO AI", "Ready to record · maximum 2 minutes per take").
  - `interview/static/app.js`: in sample mode, "Review my answer" no longer desynchronizes the flow (it advances via the same step as the primary button, else stays disabled); `addTurn` no longer re-enables it for sample turns; `reset()` restores the "Play sample answer →" label (previously stuck on "Sample complete ✓").
  - `.claude/settings.local.json` (gitignored): user asked that Chrome automation run without per-action prompts; allow rule added for `mcp__claude-in-chrome`.
- Verification (real Chrome on Windows, against the user-started Rehearsal server on 8766, PID observed, not restarted):
  - Desktop: full sample flow start → answer → coaching → retry → improved answer → comparison → download button visible; reset returns to 0 turns with correct labels; restart works. Browser speech synthesis did play (skip button appeared and advanced segments). No console errors. No duplicate DOM IDs.
  - Local practice panel opens with question select, Hear question, Record, focus field.
  - Mobile: 390px-wide same-origin iframe (window resize was not applied by the browser) — no horizontal overflow before or after the full sample flow; comparison stacks cleanly.
  - `python -m unittest test_interview` 8/8 OK; `node test_practice.cjs` PASS; `node --check` on app.js/practice.js OK.
- Open issues / unverified: did NOT click Record (Chrome mic permission prompt would block automation) — physical microphone capture/playback/download still unverified. Download click not exercised (would trigger a file download). Speech audio quality/voice not heard by agent. Live/text AI modes untouched (API deferral still in effect). Mobile check via iframe, not a real device.
- Next action: user does a 2-minute manual mic test in Local practice; then Rehearsal-specific submission materials (README/SUBMISSION/DEMO) and a first git commit + GitHub repo when user approves.

### 2026-10-22 (night) — Direction set by user; first commits
- Decision: user asked the agent to commit, write submission materials, and keep developing autonomously overnight. User rule: never credit Claude/Codex/AI as co-author anywhere (recorded in AGENTS.md; agent memory; local settings attribution disabled).
- Commits: `e7edb0e` snapshot of all prior work (trace-submission.zip and `.claude/` are gitignored).
- No remote/GitHub repository created; publishing still needs the user.

### 2026-10-22 (night) — Deterministic answer checks as MCP tools (works with no API key)
- Purpose: the core coach→retry→compare loop had no real computation without a paid key. Added transparent, deterministic wording checks so the loop and MCP tools work offline and are demonstrable.
- Changes: `interview/checks.py` (ownership "I" vs "we", I+action phrases, verification terms, vague outcomes, fillers, numeric claims to support, reflection/limits, length; exact-substring quotes; compare = per-signal count deltas with honest "no change" wording; no scores). `server.py`: MCP tools `check_answer_text`, `compare_answer_texts`; endpoints `/api/check`, `/api/compare-text` (go through the real MCP client); `coach_latest_answer` also attaches `rule_checks`. Fixed pre-existing bug: MCP tool errors were raised inside the anyio task group and surfaced as HTTP 500 "Internal Server Error"; now 400 with readable message. `test_checks.py` (8 tests), integration test extended and port-parametrized (`INTERVIEW_PORT`).
- Frontend: `static/checks.js` renderer; sample coaching/comparison show panels computed live by the MCP tools (labelled as such next to the authored feedback); local practice adds typed takes, "Check my words" per take, first-vs-latest comparison, notes export includes checks; WebM duration=Infinity player fix.
- Verification: Python 16/16 OK against agent-owned server on port 8767 (user's 8766 server left untouched, still running old code); `node test_practice.cjs` PASS (new mocked tests: typed takes, check gating, compare args, stale result after reset, 4-take limit). Headless Chrome (CDP driver in agent scratchpad, `--use-fake-device-for-media-stream`): sample panels render real MCP output (protocol 2025-11-25); local flow recorded a real 3 s MediaRecorder WebM from Chrome's FAKE mic device, playable, duration 3.36 s after fix; check/typed take/compare/reset work; 390px has no horizontal overflow; no console errors. Screenshots reviewed by agent.
- Open issues: physical microphone still not tested (fake device only). Heuristics are English-only word lists; can misfire (e.g. "profiled" counted as verification). Claude-in-Chrome extension disconnected mid-session; headless Chrome used instead.
- Next action: Rehearsal submission docs (root README, SUBMISSION, DEMO), then optional browser speech captions.

### 2026-10-22 (night) — Repo restructure and submission materials
- Purpose: make the repository judge-ready and draft all Devpost text.
- Changes: moved Trace into `trace/` (imports verified from new location; its README marked paused). New root `README.md` (status table, setup for Windows/macOS/Linux, MCP usage with a verified Python example, privacy, tests, layout, prior art). `SUBMISSION.md` (all Devpost fields, product feedback per tool, 5 friction-log entries, feature requests). `DEMO.md` (timed script <3 min, checklist, sample typed takes). `interview/README.md` updated. LICENSE holder set to Minh Dau. MCP server now publishes `instructions`, tool titles, and annotations (check tools read-only/idempotent/closed-world). Pluralization fix in check notes.
- Verification: re-read official rules via curl (WebFetch 403). Each friction entry was reproduced: tool error text prefix "Error executing tool <name>:"; exception inside client contexts → ExceptionGroup; `FastMCP.__init__` has no version parameter and serverInfo.version = 1.30.0. README Python example executed against port 8767 and printed 2025-11-25 plus JSON. Python 16/16 OK (test now asserts instructions and annotations).
- Open: GitHub repo, video, Devpost submission are user actions; `[fill in]` markers remain in SUBMISSION.md. The user's 8766 server still runs pre-overnight code.
- Next action: optional features (practice history across sessions via MCP; captions), keeping docs in sync.
