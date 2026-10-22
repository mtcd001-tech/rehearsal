# Agent continuity instructions

These instructions apply throughout this repository. The user explicitly requested persistent tracking so a fresh agent can continue without the chat history.

## Before working

1. Read `HANDOFF.md` completely. It identifies the active project, decisions, verification limits, and next steps.
2. Read the active project's README (`interview/README.md`) and the latest entries in `WORK_LOG.md`.
3. Inspect `git status` and relevant files before editing. Preserve existing user work. Do not assume a server is running, credentials work, or uncommitted files are backed up.
4. Continue the active objective unless the user changes it. The active project is Rehearsal in `interview/`; Trace at the repository root is paused.

## During and after work

- Before editing a feature, write an IN PROGRESS checkpoint in `WORK_LOG.md` naming the task, intended files, last verified state, and exact next action. Update it after each small implementation/test batch, not only at the end of a turn. A sudden usage stop may leave no chance for a final handoff.
- On resuming, inspect unfinished checkpoints against actual files and diffs. Treat unlogged or partially written changes as unverified; do not blindly redo or discard them.

- After each meaningful implementation or verification milestone, append a dated entry to `WORK_LOG.md`: purpose, files changed, checks actually run and their results, limitations, and next action.
- Update `HANDOFF.md` whenever current state, decisions, blockers, launch instructions, or next steps change. Keep it a current snapshot, not a transcript.
- Update the applicable README for user-visible behavior or setup changes.
- Before ending a turn, approaching usage/context limits, or handing off, ensure the snapshot and log reflect the actual files. Record incomplete work and the exact next step. Do not wait until the final response to preserve essential state.
- Distinguish authored sample behavior, mocked tests, and real live integration. Never describe one as another or mark unverified browser/audio behavior as tested.
- Never record secrets in documentation, logs, examples, commits, or tool output. Record credential availability/status only.
- Do not retry paid AI calls while the user's API-access deferral remains in effect. Sample/local work can continue independently.
- Do not start sub-agents merely because this file mentions multiple agents; this is a sequential handoff protocol, not authorization to delegate.
- Final updates to the user should mention the important outcome and remaining limitation, not reproduce the whole log.

## Work log entry template

```markdown
### YYYY-MM-DD — Short milestone title
- Purpose:
- Changes (paths):
- Verification (commands/results; mocked vs live):
- Open issues / unverified:
- Next action:
```

If the user changes direction, record the new decision and archive the previous plan in the log without deleting useful prior work. These instructions complement, and never override, the user's current instructions.

## Authorship rule (user instruction, 2026-10-22)

Never add Claude, Codex, or any AI tool as a co-author or "generated with" credit in commits, PR descriptions, or project docs. Commits are authored by the user's git identity only.
