# Course content

This folder is the **syllabus and reading corpus** for the Western philosophy study app. The UI lives elsewhere; it should treat these files as data.

## What to load

| File | Role |
| --- | --- |
| `course.json` | Full course: eras → units → assignments. **Source of truth.** |
| `texts/*.json` | Public-domain English texts for in-app reading. |
| `glossary.json` | Working vocabulary for the glossary tab. Load `./content/glossary.json`. |
| `schema.md` | Field-by-field contract. |

The static app also keeps a copy of the syllabus at the repo root (`/course.json`) as a fallback. Edit **`content/course.json`** first, then copy it to the root.

In-app text paths in assignments look like `texts/plato-apology.json` (relative to `content/`). Fetch them as `./content/texts/plato-apology.json`. If you add a `public/` folder, copy `texts/` there too (`public/texts/…`) without changing the path strings.

## How Samuel should use the course

Read in order. Each assignment names **exact** pages or sections, why those pages, what to look for, and questions. Later units assume earlier ones (`prerequisites` are real, not decorative). Prefer the hosted text when `text` is present; use `source.url` as the bibliographic record and as a backup if a file is missing.

After each sitting, take the **quiz** on the assignment (`quiz`). It checks the assigned move, not outside trivia. Units with three or more assignments also have a **recap quiz** (`recapQuiz`). See `schema.md` for the question object (multiple-choice default; true-false and multiple-select are used sparingly).

Bibliographic assignments (`kind: "bibliographic"`) are still required intellectually. They are not hosted. Get a library or purchased copy. Do not paste pirated prose into this repo.

## Public-domain sourcing rules

Hosted files must be **English** and **public domain in the US**.

Preferred legal sources (verified before ingest):

- [Project Gutenberg](https://www.gutenberg.org/)
- [Wikisource](https://en.wikisource.org/)
- [Internet Classics Archive (MIT)](https://classics.mit.edu/)
- [Perseus Digital Library](https://www.perseus.tufts.edu/)
- [Standard Ebooks](https://standardebooks.org/) (PD works only)
- [Internet Archive](https://archive.org/) when the item is clearly PD
- [CCEL](https://www.ccel.org/) and [New Advent](https://www.newadvent.org/summa/) for PD translations of Anselm, Aquinas, Plotinus, etc.

Rules:

1. Do not invent URLs. Confirm the work exists at the cited address.
2. Do not ingest a translation that is still in copyright even if the original is ancient.
3. Strip Gutenberg/CCEL license **boilerplate** from `sections[].paragraphs`. Keep credit in `source` and `attribution`.
4. Prefer the **assigned sitting** (20–90 minutes) over dumping a 400-page book. Store a whole short work (Apology, Crito, Enchiridion, Enquiry sections assigned). For long books, store the assigned stretch plus enough context to read as one sitting.
5. Keep standard locators (Stephanus, Bekker, Kant Ak, book/chapter) on `section.locator`.
6. Never scrape or paste in-copyright late-20th/21st-c. prose. Cite it; set `source.available: false`.

US rule of thumb used here (2026): publication year + 95 years. Works published **1929 and earlier** are PD; **1930** entered PD in 2026. Restored foreign copyrights (URAA) still block some 1920s works whose authors died recently enough that the source country was in term on 1 January 1996 (e.g. Heidegger). When in doubt, mark bibliographic and do not host.

## Regenerating texts

Raw downloads (not shipped) live in `content/_raw/` if you run the ingest helper. Hosted JSON is hand-checked after parse:

```bash
python3 -m json.tool content/course.json > /dev/null
python3 -m json.tool content/texts/plato-apology.json > /dev/null
python3 scripts/validate-course.py
```

## Coordination with the app

- Stable course `id`: `western-philosophy`.
- Do not renumber `assignment.id` values once students have progress in `localStorage`.
- Optional fields (`translator`, `themes`, `text`, `source.locator`) may be missing; the UI must not crash.
- `text` is the signal to render an in-app reader. If it is absent, fall back to `source.url` or the bibliographic panel.
