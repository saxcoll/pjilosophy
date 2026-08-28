# pjilosophy

A static study app for a Western philosophy directed-reading course. It tells you **exactly what to read next** — work, selection, pages, and why those pages come now — and keeps progress in this browser.

No login. No server. Public-domain readings open **in the app**. In-copyright items are cited, not hosted.

## Run locally

From the repository root:

```bash
python3 -m http.server 8080
```

Then open [http://127.0.0.1:8080](http://127.0.0.1:8080).

Any static server in the repo root works (`npx --yes serve .` if you have Node). Open the site at the server’s origin, not as a `file://` page, so `course.json` can load.

## Live site

**https://saxcoll.github.io/pjilosophy/**

GitHub Pages is enabled from `main` / root (`/`). No build step; this is a static site. Asset and JSON URLs are relative (`./assets/…`, `./content/course.json`), so they work under `/pjilosophy/`.

## Course data

The UI fetches both files and uses the **larger syllabus** (more assignments, then more quizzes). A leftover stub cannot win if the full course is present.

1. `./content/course.json` — source of truth
2. `./course.json` — fallback copy (kept in sync by `content/tools/build_course.py`)

Home recommends the first unread assignment on that list.

Public-domain texts live in `content/texts/<id>.json`. Assignments may point at them with a `text` object (`id`, `path`, optional `start` / `end`). The reader loads those files over relative URLs (`./content/texts/…`), so GitHub Pages under `/pjilosophy/` still works.

Progress key: `pjilosophy.progress.v1` in `localStorage` (completion, notes, reader scroll, and quiz scores). Quizzes live on assignments as `quiz` and on units as `recapQuiz`; open **Quizzes** in the header. **Terms** is the course glossary (`content/glossary.json`).

## Layout

```
index.html              app shell
assets/app.js           routing, progress, views
assets/styles.css
assets/favicon.svg
content/course.json     syllabus (source of truth when present)
content/glossary.json   course glossary for the Terms tab
content/texts/          public-domain reading JSON
course.json             fallback copy of the syllabus
scripts/validate-course.py
```
