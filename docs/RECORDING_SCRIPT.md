# Demo recording script: step by step, with exact words

**Goal:** a video under 3:00, target 2:45. Record the real flow once (5–8 minutes of raw footage), then cut it down and add the narration.

## A. Setup (10 minutes, before you press record)

1. **Gemini key:** put the new key in `interview\.env` (`GEMINI_API_KEY=...`). Close that file, so it never appears on screen.
2. **Restart the server:** Ctrl+C in its terminal, then run `.venv\Scripts\python interview\server.py`.
3. **Chrome:**
   - Open `http://127.0.0.1:8766` in a clean window.
   - Close other tabs. Hide bookmarks with Ctrl+Shift+B.
   - Zoom to 110% with Ctrl and +.
4. **Audio:** wear headphones, so Maya's voice doesn't loop back into your microphone.
5. **Fill in Interview setup with fictional, non-sensitive details:**
   - **Role:** Software Engineering Intern
   - **Company:** a product engineering team
   - **Experience** (paste this):
     > Computer science student. Built a campus events app in a three-person team. Owned the search endpoint and wrote API tests. Python, PostgreSQL, React.
   - **Round:** Behavioral. **Length:** 5 minutes.
   - **Skills to improve:** explaining my own contribution clearly.
   - Press **Save**.
6. **Do one silent rehearsal run:** a full 5-minute interview, End, debrief, replay. Make sure everything works today before recording.
7. **Screen recorder:** Windows Game Bar (press **Win+Alt+R** to start and stop; it records the Chrome window plus its audio) or OBS. Check that Maya's voice is in the recording.

## B. Record the raw footage (one continuous take)

Just do the flow naturally. Don't narrate yet; narration is easier added afterward. If you prefer speaking live, the lines are in section C.

1. **Home page:** hold for 3 seconds, slowly hover the three "Interview / Debrief / Pressure Replay" cards.
2. Open **Interview setup** and scroll through it slowly (about 5 seconds), then close it.
3. **Enter interview room:**
   - Tick **Show my camera**, choose **5 minutes**, then press **Allow microphone & begin**.
4. **Answer Maya's first question.** Say this answer on purpose. It's intentionally vague, so the debrief has something real to catch:
   > "Sure. In my club project we built an events app for our campus, and search was really slow. We worked on the database and made it a lot faster. It worked well and the team was happy with it."
5. **Maya will probably follow up**, for example "What did you personally do?". Answer honestly and briefly:
   > "I mostly worked on the search query. I changed how it fetched data. I didn't measure it exactly, but it felt faster."
6. Answer one more question naturally if she asks one, then press **End interview**.
7. **Debrief** (it may take 10–30 seconds to generate, which you'll cut later):
   - Scroll slowly through the summary and *Keep doing / Work on next*.
   - Stop on **Why Maya asked that** for 5 seconds.
   - Expand one answer.
8. **Pressure Replay:** scroll to the card, pick the moment, then press **Start 90-second replay**.
9. **Replay answer:** when Maya repeats the question, give the improved version:
   > "I owned the search endpoint for our campus events app. Search was slow, so I profiled the query and found we were fetching every column for every event. I limited it to the fields we needed and added an index on the event date. I tested it with our sample data. Search went from a few seconds to under a second on my laptop, though I didn't run a formal benchmark."
10. **Maya changes a condition**, for example "What if there were ten times more events?". Think out loud, briefly and honestly. For example:
    > "Then I'd measure first. I'd check the query plan, add pagination so we never load everything, and consider caching the most common searches."
11. Press **End replay**. On the comparison:
    - Show the verdict, the **BEFORE / RETRY** quotes and the **Did your retry resolve the open question?** line.
    - Expand **Wording comparison · MCP tool**.
12. Click **Download transcript & review**, then **Back to practice**. Stop recording.

If the replay or the debrief fails, keep recording and see section E.

## C. Cut to about 2:45 and narrate

Use Clipchamp, which comes with Windows (or any editor). Cut the waiting time and add a small caption wherever you cut, for example "cut: review generating" or "interview excerpt".

| Time | On screen | Say (or record as voiceover) |
|---|---|---|
| 0:00–0:12 | Home page, hover the three cards | "Interviews are hard to practice alone. The hard part isn't the first answer; it's the follow-up. Rehearsal is a mock interview that follows up like a real one, then shows you exactly what to fix." |
| 0:12–0:25 | Setup dialog | "I give it the role and my experience. Resumes are extracted on my own computer, and the interviewer uses this to tailor the questions." |
| 0:25–0:35 | Consent screen, then *Allow microphone & begin* | "This is a timed, hands-free interview. My camera stays on my screen only. Only my audio goes to Gemini Live." |
| 0:35–1:05 | Room: your first answer, Maya's follow-up, your reply, *End interview*. Caption: "Interview excerpt". | *(Let the real audio play; no narration over it.)* Optional, over the follow-up: "Notice she didn't move on. She asked what I personally did." |
| 1:05–1:30 | Debrief, stopping on **Why Maya asked that** | "Feedback only comes at the end, and it quotes my exact words. Here's the part I like: why Maya asked that follow-up. I said 'we worked on the database'. It was unclear what I did myself, so she asked. Every quote is checked against the real transcript." |
| 1:30–2:05 | Pressure Replay: start, Maya's question, your improved answer, the changed condition, your reply. Caption: "Replay excerpt". | "Instead of just reading advice, I replay that exact moment. Maya repeats the question, and then she changes one condition, so I have to reason, not recite." *(Then let the audio play.)* |
| 2:05–2:30 | Comparison: verdict, BEFORE vs RETRY, Resolved line, MCP wording panel | "The comparison shows what actually changed, using my own words: 'we worked on the database' became 'I profiled the query and added an index.' It says whether I resolved the open question, and what's still worth asking. This wording check comes from our self-hosted MCP server, and it can also say 'no improvement'. There are no fake scores." |
| 2:30–2:45 | Back to the home page, or the GitHub repo page | "Rehearsal: interview, see why the follow-ups came, then retry the moment that mattered. It's a self-hosted MCP server, spec 2025-11-25, plus a web simulation of an Alexa+-style voice experience. The code is open source on GitHub." |

**Important: read what is actually on screen.**
- If the verdict says "Mixed" or "Not yet" instead of "Clearer", say that ("it says I only partly fixed it"). That honesty is a strength.
- Don't claim improvement the app didn't report.

## D. Upload

1. Export at 1080p. Check that the length is **under 3:00**.
2. Upload to YouTube with visibility set to **Public**. Unlisted may not count; the rules say "publicly visible".
3. **Title:** "Rehearsal: mock interviews that follow up like a real one (Alexa+ track)".
4. **Description:** paste the tagline and the repo link, https://github.com/mtcd001-tech/rehearsal.
5. Use no copyrighted music. Silence or YouTube's free audio library is fine.
6. Paste the link into Devpost, and send it to me so I can add it to `SUBMISSION.md`.

## E. If something fails while recording

- **The debrief shows a Gemini error:** press **Try analysis again**. It keeps your transcript.
- **The replay doesn't appear, or fails:** show the interview and the debrief, then say: "Pressure Replay is implemented, but it didn't run in this recording." Fill the remaining time with the authored sample: *Practice a single answer or explore the demo* → *Experience the sample* → the coaching with its `check_answer_text` MCP panel → retry → `compare_answer_texts`. Say on screen that it's an **authored sample**.
- **Live voice doesn't work at all:** record only the authored sample plus the MCP App preview (footer → *MCP App preview* → *Call check_answer_text*), and explain why live voice couldn't be shown.
- **Never** show the mock harness or anything labelled `[MOCK]`.

## F. Final checks before submitting

- [ ] The video is under 3:00, public, and its link is in Devpost.
- [ ] No API key, `.env` or personal information is visible.
- [ ] Cuts and excerpts are captioned.
- [ ] You didn't claim it runs inside a real Alexa.
