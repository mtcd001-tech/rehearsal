# Submission checklist (deadline: Fri Oct 23, 12:00 p.m. PT / 3:00 p.m. ET)

Everything below needs you: publishing, recording, and submitting are your actions. The rest is done and committed on `main`.

## 1. Test the latest version yourself (15 min)

Restart the server so it runs the latest code. Press Ctrl+C in its terminal, then:

```powershell
cd D:\hackamazon
.venv\Scripts\python interview\server.py
```

Open http://127.0.0.1:8766, refresh, and put on headphones.

1. **The most important test.** *Enter interview room* → choose **5 minutes** → *Allow microphone & begin*. Answer two or three questions out loud, then press *End interview*. Check the following:
   - Maya speaks.
   - She hears you and follows up.
   - The debrief appears.
   - *Download transcript & review* works.

   This is the one thing nobody has tested with a physical microphone yet. If it fails, note the message shown and use the no-key path in `DEMO.md`.
2. Optional: under *Practice a single answer or explore the demo*:
   - Run **Experience the sample** through to the comparison.
   - In **Practice my own answer**, record one take and analyze it with Gemini.
3. Footer → **MCP App preview** → **Call check_answer_text**.

## 2. Review the text (15 min)

- `README.md`: the judge-facing overview.
- `SUBMISSION.md`: paste into Devpost. Fill in every **[fill in]**.
- `DEMO.md`: the video script.

Change anything that doesn't sound like you.

## 3. Publish the code (5 min)

1. On github.com, create a **public**, **empty** repository (no README or license; the repo has them). For example, name it `rehearsal`.
2. Push:

   ```powershell
   cd D:\hackamazon
   git remote add origin https://github.com/<your-username>/rehearsal.git
   git push -u origin main
   ```

3. Check that the repo page shows **MIT license** in the About sidebar.

Commits are authored by your git identity only (Minh Dau).

## 4. Record the demo (20–30 min)

- Follow `DEMO.md`. Keep it **under 3:00**. Label the interview clip as an excerpt. (The old silent AVI in `demo-video/` predates the redesign; don't use it.)
- Upload to YouTube or Vimeo as **Public**.
- Use no copyrighted music.

## 5. Submit on Devpost (15 min)

- **Track:** Alexa+.
- **Repo URL:** your new repository.
- **Video URL:** your upload.
- **Gallery:** upload the images listed in `SUBMISSION.md` from `docs/screenshots/`.
- **Text:** paste the sections from `SUBMISSION.md`, including product feedback and the friction log (the friction log can earn up to a 10% bonus).

Submit before **12:00 p.m. PT**. Leave a buffer.

## Do not

- Claim the live AI voice interview works. It has not been verified (the API key had no quota).
- Change the submitted code, video or materials after the deadline. The organizers ask entrants to freeze them until winners are announced.
