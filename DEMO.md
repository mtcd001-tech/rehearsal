# Rehearsal — demo video script (target 2:45, hard limit under 3:00)

**Before recording:**
- Restart the server: `.venv\Scripts\python interview\server.py`.
- Open `http://127.0.0.1:8766` in Chrome and use headphones.
- Do one 5-minute practice interview first, to confirm your microphone, Gemini Live quota and the debrief all work.
- Use a fictional or non-sensitive resume and job description.
- Keep no API key, `.env` or personal contact details on screen.
- Use no copyrighted music.

**Honesty rules for the video:**
- The interview segment is an **excerpt** of a longer session. Say so, or show yourself pressing *End interview*.
- Do not imply that a shortened clip is a full 30-minute run.
- If you edit out wait times, add a caption such as "cut: review generating".
- Do not show company research as working unless it works when you record; it returned HTTP 429 during our testing.

| Time | On screen | Say (in your own words) |
|---|---|---|
| 0:00–0:15 | Home page | "Internship candidates practice answers alone, but real interviews have follow-ups, and most feedback is a score or 'use STAR'. Rehearsal is a timed mock interview, plus feedback that quotes your own words." |
| 0:15–0:35 | *Interview setup*: role, company, job description, resume upload (fictional), round, length. Close. | "I give it the job and my experience. The resume is extracted locally; I review it before it's used." |
| 0:35–0:50 | *Enter interview room* → consent screen → *Allow microphone & begin* | "It tells me exactly what goes to Google: my audio and setup, for Gemini Live. No coaching during the interview." |
| 0:50–1:40 | The room: Maya asks, you answer for about 30 s, Maya follows up on your answer, you reply briefly. Then press **End interview**. | "No buttons between answers. Maya follows up on what I actually said, like a real interviewer. This is an excerpt; I'm ending it early." |
| 1:40–2:10 | Debrief: summary, *Work on next*, then expand one answer showing your quoted line, how to improve it, and a clearer version. | "Feedback only after the interview. It quotes my exact words; quotes are checked against the transcript, with no scores. The clearer version is a suggestion I still fact-check." |
| 2:10–2:35 | *Back to practice* → *Practice a single answer or explore the demo* → run the sample to the `check_answer_text` panel, then the retry comparison. | "Under the hood, a self-hosted MCP server — spec 2025-11-25 — runs deterministic checks with no key: 'we' instead of 'I', no verification, vague outcomes. Then it shows whether the retry actually changed." |
| 2:35–2:50 | Footer → *MCP App preview* → *Call check_answer_text*; or run `.venv\Scripts\python interview\agent_sim.py --demo` | "The same tools render as an MCP Apps card, so an assistant like Alexa+ could run this loop by voice. Alexa+ itself wasn't available to test, so this is a simulation." |

## If the live interview is not working when you record

Use the no-key path:

1. The sample (0:15–1:40): authored answer → follow-up → coaching with the live `check_answer_text` panel → retry → `compare_answer_texts`.
2. Practice my own answer: a typed take, then *Check my words*.
3. The MCP App preview.

Say on screen that the live interview is implemented but could not be shown, and why (for example, quota). Do not use mocked output.

The silent captioned AVI in `demo-video/` (git-ignored) **predates the redesign and the interview room**. Do not use it for the submission.

## Recording checklist

- [ ] Server restarted; page reloaded; 5-minute practice interview completed successfully.
- [ ] Fictional setup data only; no key, `.env` or personal data visible.
- [ ] The interview clip is labelled as an excerpt, or shows *End interview*.
- [ ] The words "authored sample" and "computed now by the … MCP tool" are visible during the sample segment.
- [ ] Video under 3:00, uploaded publicly to YouTube or Vimeo; link pasted into `SUBMISSION.md` and Devpost.

## Pressure Replay demo option (target2:45)

After browser-checking the new feature, use this tighter sequence instead of adding to the script above:

- 0:00-0:15: problem and setup.
- 0:15-0:55: short excerpt of the live interview; one answer and follow-up, then show End interview.
- 0:55-1:15: debrief quote and one improvement focus; choose Pressure Replay.
- 1:15-2:10: replay excerpt: original question, clearer spoken retry, changed-condition follow-up and brief answer. Label any cuts; show whether the replay ended automatically or was ended early.
- 2:10-2:35: actual before/after quotes and separate follow-up feedback. Expand Wording comparison to show the real MCP tool output.
- 2:35-2:45: close: practice the difficult moment, then test your understanding under a changed condition.

Use actual results, including an unresolved issue if that is what the model reports. Synthetic tests verified the provider path; rehearse the new browser flow before recording. Five-minute interview/webcam were already confirmed by the user; full30-minute testing is not a submission blocker.
