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
