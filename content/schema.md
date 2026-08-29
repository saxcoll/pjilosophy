# Course and in-app text schema

The study app reads **`content/course.json`** (syllabus) and, for public-domain assignments, **`content/texts/<id>.json`** (the English reading itself). Paths in the syllabus are relative to `content/`. The working vocabulary is **`content/glossary.json`**.

Canonical files:

- `content/course.json` — source of truth for the sequence
- `content/texts/*.json` — hosted public-domain readings
- `content/glossary.json` — philosophical terms for the glossary tab
- `content/thinkers.json` — names, ids, and portrait credits
- `content/images/thinkers/` — hosted public-domain / CC portraits
- `course.json` (repo root) — copy of the syllabus for the static app fallback

Do not duplicate copyrighted prose. Bibliographic assignments have no `text` object.

---

## `course.json`

```text
{
  course: { id, title, subtitle, description, audience, estimatedHours, method, tracks? },
  eras: [ Era, ... ]
}
```

### `course`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Stable kebab-case. This course is `western-philosophy`. |
| `title`, `subtitle`, `description` | string | Shown on Home / Syllabus. |
| `audience` | string | Who the sequence is for. |
| `estimatedHours` | number | Whole-course estimate. |
| `method` | string | 2–4 paragraphs: how to use the course. |
| `tracks` | Track[] \| omitted | Optional thematic threads that reuse existing assignment ids in a different order. |

### `Track`

A first-class path across eras. The chronological syllabus stays the source of reading order; a track is a professor-designed subset.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique kebab-case. This course includes `science-epistemology`. |
| `title`, `subtitle` | string | Shown if the UI lists tracks. |
| `intro` | string | Why the thread exists; how earlier sittings set up later ones. |
| `assignmentIds` | string[] | Existing assignment ids, in pedagogical order for this thread. Do not duplicate sittings; point at ids already in an era. |

Assignments listed here are also tagged `trackIds` on the assignment object.

### `Era`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique kebab-case. |
| `order` | number | Pedagogical order (1-based). |
| `title` | string | |
| `years` | string | Human range, e.g. `c. 600–450 BCE`. |
| `intro` | string | 1–3 paragraph lecture. |
| `themes` | string[] | Short tags. |
| `thinkers` | `{id, name}[]` | Philosophers this era studies. Primary first. Ids match `content/thinkers.json`. |
| `units` | Unit[] | |

### `Unit`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique kebab-case. |
| `order` | number | Order inside the era. |
| `title` | string | |
| `professorNote` | string | Why this unit exists; how it prepares the next. |
| `thinkers` | `{id, name}[]` | Philosophers this unit studies. If the unit is named around one person, that person is first. |
| `assignments` | Assignment[] | |
| `recapQuiz` | Quiz \| omitted | On units with 3+ assignments: 4–6 questions spanning the unit. |

### `Assignment`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique across the whole course. |
| `order` | number | Order inside the unit. |
| `kind` | string | `primary` \| `secondary` \| `bibliographic` |
| `title` | string | Assignment title (what to do now). |
| `author`, `work` | string | Display name of the writer (not empty). Dialogues may read e.g. `Plato (Socrates as speaker)`. |
| `thinkerId` | string \| omitted | Matches a thinker `id` (and portrait) in `content/thinkers.json`. |
| `translator` | string | English translator of the hosted or cited edition. |
| `selection` | string | What part of the work. |
| `pages` | string | Human locator: Stephanus, Bekker, Ak, chapters, Gutenberg paragraphs. |
| `estimatedMinutes` | number | Sitting length. |
| `wordCount` | number \| omitted | Words in the **assigned** hosted English (honor `text.start` / `text.end`). Present on public-domain in-app readings when countable. **Omit** rather than invent a fake precise number. Bibliographic / in-copyright sittings usually omit this. |
| `difficulty` | number | Integer **1**, **2**, or **3**. **1** accessible (e.g. Plato’s *Apology*, *Crito*, a short Mill selection). **2** intermediate (e.g. Hume *Enquiry* chunks, Descartes *Meditations*, Aristotle *NE* I). **3** advanced (e.g. Spinoza *Ethics*, Kant *Critique of Pure Reason*, Aristotle *Metaphysics*, Hegel, Tractatus density). Required on every assignment. |
| `trackIds` | string[] \| omitted | Ids of `course.tracks` this sitting belongs to (e.g. `["science-epistemology"]`). Omitted when the sitting is not on a track. |
| `why` | string | Why these pages, why now. |
| `lookFor` | string[] | 2–4 reading cues. |
| `questions` | string[] | 2–4 questions. |
| `prerequisites` | string[] | Assignment ids. Empty only for the first item. |
| `nextHint` | string | What this prepares. |
| `source` | Source | Legal source of the work. |
| `text` | TextPointer \| omitted | Present only when a public-domain file is hosted in-repo. |
| `quiz` | Quiz \| omitted | Check after the sitting. Required on every assignment that has a real reading (including bibliographic). |

Global reading order is `era.order`, then `unit.order`, then `assignment.order`. After the assignment quiz, a unit with three or more assignments may also have `recapQuiz`.

### `Quiz` (`assignment.quiz` and `unit.recapQuiz`)

Same object shape in both places. Assignment quizzes have 3–5 questions; unit recap quizzes have 4–6 and span the unit.

```json
{
  "id": "plato-apology-quiz",
  "title": "After Apology",
  "intro": "One or two sentences: what this check is for.",
  "questions": [
    {
      "id": "q1",
      "type": "multiple-choice",
      "prompt": "Question stem about the assigned pages.",
      "options": [
        { "id": "a", "text": "…" },
        { "id": "b", "text": "…" },
        { "id": "c", "text": "…" },
        { "id": "d", "text": "…" }
      ],
      "correct": "b",
      "explanation": "Short professor note: why this answer, citing the move in the text."
    }
  ]
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique kebab-case. Assignment quizzes are `{assignment.id}-quiz`. Recaps are `{unit.id}-recap`. |
| `title` | string | Shown above the questions. |
| `intro` | string | What the check is for — not a lecture. |
| `questions` | Question[] | |

### `Question`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique inside the quiz (`q1`, `q2`, …). |
| `type` | string | `multiple-choice` (default) \| `true-false` \| `multiple-select`. |
| `prompt` | string | Answerable from the assigned sitting, aligned with that assignment’s `lookFor` / `questions`. |
| `options` | `{id, text}[]` | `multiple-choice`: four options, ids `a`–`d`. `true-false`: `[{id:"true",text:"True"},{id:"false",text:"False"}]`. `multiple-select`: at least four options, ids as given. |
| `correct` | string \| string[] | Option id, or an array of option ids when `type` is `multiple-select` (at least two). |
| `explanation` | string | Teaches why — cite the move in the text. Not “correct because it is correct.” |

Wrong options should be plausible misreadings, not jokes. Bibliographic / in-copyright sittings still get a quiz on the assigned ideas; do not quote long in-copyright prose in stems or options.

### `recapQuiz` (`unit.recapQuiz`)

Optional on a unit that has **three or more** assignments. Same `Quiz` schema as `assignment.quiz`. Use it to check the unit’s arc (e.g. Euthyphro–Apology–Crito as one practice), not to repeat a single sitting.

| Field | Type | Notes |
| --- | --- | --- |
| *(same as Quiz)* | | Present on large units in this course; omitted on two-assignment units. |

### `Source`

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | Gutenberg, Wikisource, MIT Classics, etc. |
| `url` | string | Legal page. Never a pirate scan. |
| `locator` | string | Chapter/fragment/Stephanus hint. |
| `license` | string | `public-domain` \| `in-copyright` \| `unknown` |
| `available` | boolean | `true` only if a legal full-text URL was verified. |
| `edition` | string | Short citation. |
| `note` | string | Optional. Required in spirit for bibliographic items (library/legal copy). |

`kind: "bibliographic"` items must have `source.available: false`, `source.license: "in-copyright"` (or `unknown` if the status is messy), and **no** `text` object.

### `TextPointer` (`assignment.text`)

Points at a file under `content/texts/` so the app can render the reading without leaving the site.

```json
{
  "id": "plato-apology",
  "path": "texts/plato-apology.json",
  "format": "json",
  "scope": "full",
  "start": null,
  "end": null,
  "locator": "entire dialogue, Stephanus 17a–42a"
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Matches the text file’s `id`. Several assignments may share one file (e.g. split Meditations). |
| `path` | string | Relative to `content/`, always `texts/<id>.json`. |
| `format` | string | Always `json` in this course. |
| `scope` | string | `full` = this assignment is the whole stored file (or the whole short work). `excerpt` = jump to `start`/`end` inside a longer stored file. |
| `start`, `end` | string \| null | `sections[].id` values in the text file. Inclusive range. `null` when `scope` is `full`. |
| `locator` | string | Shown in the reader: “you are reading Republic 514a–521b”. |

The app should load `./content/` + `path` (for example `./content/texts/plato-apology.json`). If it copies files to `public/texts/`, keep the same filenames.

---

## Text files (`content/texts/<id>.json`)

One file per work, or per coherent excerpt bundle from a long work.

```json
{
  "id": "plato-apology",
  "title": "Apology",
  "author": "Plato",
  "translator": "Benjamin Jowett",
  "language": "en",
  "license": "public-domain",
  "source": {
    "name": "Project Gutenberg",
    "url": "https://www.gutenberg.org/ebooks/1656",
    "edition": "Jowett; Project Gutenberg EBook #1656"
  },
  "attribution": "Plato, Apology, trans. Benjamin Jowett. Public domain. Source: Project Gutenberg.",
  "sections": [
    {
      "id": "s1",
      "locator": "17a–18a",
      "heading": "Opening of the defense",
      "paragraphs": ["…", "…"]
    }
  ]
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Filename without `.json`. |
| `title`, `author`, `translator` | string | |
| `language` | string | Always `en`. |
| `license` | string | Always `public-domain` for hosted files. |
| `source` | object | `name`, `url`, `edition` of the ingested edition. |
| `attribution` | string | Credit line for the reader footer. |
| `sections` | Section[] | Reading body, Gutenberg headers/footers stripped. |

### `Section`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Stable, unique inside the file. Used as `assignment.text.start` / `end`. |
| `locator` | string | Stephanus, Bekker, Ak, book/chapter, fragment numbers — what the student should see. |
| `heading` | string | Optional display heading. |
| `paragraphs` | string[] | Body paragraphs. No license boilerplate. |

---

## Kind and license rules

| Situation | `kind` | `source.available` | `source.license` | `text` |
| --- | --- | --- | --- | --- |
| Hosted PD reading | `primary` or `secondary` | `true` | `public-domain` | required |
| PD work, legal URL, not yet ingested | `primary` | `true` | `public-domain` | omit |
| In-copyright assigned reading | `bibliographic` | `false` | `in-copyright` | omit |

US public-domain cutoff used for this course (as of 2026): works **published 1930 or earlier** in the United States. Foreign works still in copyright in the source country on 1 Jan 1996 may be restored (URAA). Translations have their own term: a PD Greek original does not make a 1990s English translation hostable.

---

## Glossary (`content/glossary.json`)

Source of truth for the glossary tab. The app should load **`./content/glossary.json`**. There is no root fallback copy (unlike `course.json`); do not duplicate this file at the repo root unless the UI agent later mirrors the course-file pattern.

```text
{
  title, intro,
  terms: [ Term, ... ]
}
```

### `Term`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique kebab-case lemma (`eudaimonia`, `categorical-imperative`). |
| `term` | string | Display heading. |
| `sortKey` | string | Alphabetical sort (usually the `id`, or a phrase without a leading “the”). |
| `aliases` | string[] | Other names to search or show (`happiness (Aristotle)`, `flourishing`). May be empty. |
| `short` | string | One sentence for list/scan — the margin gloss. **Required.** |
| `definition` | string | 2–4 sentences. Precise seminar voice. English, with Greek/Latin when it matters. |
| `eraIds` | string[] | Actual `era.id` values from `course.json` (e.g. `ancient-classical`). A term may belong to more than one era if it evolves. |
| `unitIds` | string[] | Actual `unit.id` values. |
| `assignmentIds` | string[] | Actual `assignment.id` values where the word is load-bearing. |
| `seeAlso` | string[] | Other **term ids** that exist in this file. May be empty. |
| `firstAppearsIn` | string | Assignment id where Samuel should meet the word. Must be one of `assignmentIds`. |

This is a working vocabulary for the 11-era course, not a general philosophy dictionary. Bibliographic / in-copyright sittings are defined from the assignment’s framing; do not quote long in-copyright prose in `short` or `definition`.

---

## Thinkers and portraits (`content/thinkers.json`)

Catalog of philosophers the syllabus names. The app should load **`./content/thinkers.json`**. Image paths are relative to `content/` (for example `images/thinkers/plato.jpg` → `./content/images/thinkers/plato.jpg`). Files live in `content/images/thinkers/`. Only public-domain or Wikimedia CC BY / CC BY-SA images are stored.

```text
{
  thinkers: [ { id, name, sortName, image?, imageCredit?, license? }, ... ]
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Kebab-case. Same ids as `era.thinkers[].id`, `unit.thinkers[].id`, and `assignment.thinkerId`. |
| `name` | string | Display name. |
| `sortName` | string | Sort key (usually surname, or the one-word name). |
| `image` | string \| omitted | Path relative to `content/`, when a free portrait is hosted. |
| `imageCredit` | string \| omitted | Title, artist or photographer, license, Wikimedia page URL. |
| `license` | string \| omitted | `public-domain` \| `cc-by` \| `cc-by-sa`. |

Eras and units list the thinkers they study so the UI can show names (and portraits) prominently. Primary thinker first.


