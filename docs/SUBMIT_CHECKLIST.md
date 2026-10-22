# Submission checklist (deadline: Fri Oct 23, 12:00 p.m. PT / 3:00 p.m. ET)

Everything below needs you: publishing, recording, and submitting are your actions. The rest is done and committed on `main`.

## 1. Look at the latest version (10 min)

The server you started earlier is still running old code. Restart it:

```powershell
# in the terminal running the old server: Ctrl+C, then
cd D:\hackamazon
.venv\Scripts\python interview\server.py
```

Open http://127.0.0.1:8766 and try the following:

1. **Experience the sample**, all the way to the comparison.
2. **Practice my own answer**:
   - Record a real take with your microphone (this has not been tested with a physical mic yet).
   - Write what you said, then press **Check my words**.
   - Make a second take, then press **Compare first and latest take**.
3. Optionally tick **Draft a transcript while I speak** to see whether Chrome's captions work for you. In Chrome this sends audio to Google, and the app says so.
4. Footer → **MCP App preview** → **Call check_answer_text**.

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

- Follow `DEMO.md`. Keep it **under 3:00**.
- Upload to YouTube or Vimeo as **Public**.
- Use no copyrighted music.

## 5. Submit on Devpost (15 min)

- **Track:** Alexa+.
- **Repo URL:** your new repository.
- **Video URL:** your upload.
- **Gallery:** upload images from `docs/screenshots/`.
- **Text:** paste the sections from `SUBMISSION.md`, including product feedback and the friction log (the friction log can earn up to a 10% bonus).

Submit before **12:00 p.m. PT**. Leave a buffer.

## Do not

- Claim the live AI voice interview works. It has not been verified (the API key had no quota).
- Change the submitted code, video or materials after the deadline. The organizers ask entrants to freeze them until winners are announced.
