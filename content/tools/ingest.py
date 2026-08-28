#!/usr/bin/env python3
"""Download public-domain sources and write content/texts/*.json.

Run from repo root:
    python3 content/tools/ingest.py
"""
from __future__ import annotations

import html
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
RAW = CONTENT / "_raw"
TEXTS = CONTENT / "texts"

UA = "pjilosophy-course-ingest/1.0 (educational; local study app)"
CTX = ssl.create_default_context()


def fetch(url: str, dest: Path, retries: int = 3) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 400:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last_err: Exception | None = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=90) as resp:
                data = resp.read()
            dest.write_bytes(data)
            return dest
        except Exception as err:  # noqa: BLE001 — network is flaky
            last_err = err
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"failed {url}: {last_err}")


def pg_strip(text: str) -> str:
    start = re.search(r"\*\*\*\s*START OF (THIS|THE) PROJECT GUTENBERG EBOOK.*?\*\*\*", text, re.I | re.S)
    end = re.search(r"\*\*\*\s*END OF (THIS|THE) PROJECT GUTENBERG EBOOK.*?\*\*\*", text, re.I)
    if start:
        text = text[start.end() :]
    if end:
        text = text[: end.start()]
    return text.strip()


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ").replace("\ufeff", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class _HTMLText(HTMLParser):
    skip = {"script", "style", "noscript"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag in self.skip:
            self._skip += 1
        if tag in {"p", "h1", "h2", "h3", "h4", "br", "div", "tr", "li", "blockquote"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.skip and self._skip:
            self._skip -= 1
        if tag in {"p", "h1", "h2", "h3", "h4", "div", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        self.parts.append(data)


def html_to_text(raw: str) -> str:
    parser = _HTMLText()
    parser.feed(raw)
    return normalize("".join(parser.parts))


def paragraphs(text: str, min_len: int = 40) -> list[str]:
    chunks = re.split(r"\n\s*\n", normalize(text))
    out: list[str] = []
    for chunk in chunks:
        line = re.sub(r"\s+", " ", chunk).strip()
        if len(line) >= min_len:
            out.append(line)
        elif line and out and len(line) < min_len:
            # keep short headings attached if they look like titles
            if line.isupper() or line[:1].isalpha() and len(line) < 80:
                out.append(line)
    return [p for p in out if p]


def section(sid: str, locator: str, heading: str, paras: list[str]) -> dict:
    return {
        "id": sid,
        "locator": locator,
        "heading": heading,
        "paragraphs": paras,
    }


def dump_text(
    *,
    tid: str,
    title: str,
    author: str,
    translator: str,
    source_name: str,
    source_url: str,
    edition: str,
    sections: list[dict],
    attribution: str | None = None,
) -> Path:
    TEXTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": tid,
        "title": title,
        "author": author,
        "translator": translator,
        "language": "en",
        "license": "public-domain",
        "source": {"name": source_name, "url": source_url, "edition": edition},
        "attribution": attribution
        or f"{author}, {title}, trans. {translator}. Public domain. Source: {source_name}.",
        "sections": [s for s in sections if s.get("paragraphs")],
    }
    path = TEXTS / f"{tid}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def gutenberg_txt(ebook_id: int) -> str:
    urls = [
        f"https://www.gutenberg.org/cache/epub/{ebook_id}/pg{ebook_id}.txt",
        f"https://www.gutenberg.org/files/{ebook_id}/{ebook_id}-0.txt",
        f"https://www.gutenberg.org/ebooks/{ebook_id}.txt.utf-8",
    ]
    dest = RAW / f"pg{ebook_id}.txt"
    last = None
    for url in urls:
        try:
            fetch(url, dest)
            text = dest.read_text(encoding="utf-8", errors="replace")
            if "Project Gutenberg" in text or len(text) > 2000:
                return pg_strip(text)
        except Exception as err:  # noqa: BLE001
            last = err
            if dest.exists():
                dest.unlink()
    raise RuntimeError(f"gutenberg {ebook_id}: {last}")


def gutenberg_html(ebook_id: int, file_hint: str | None = None) -> str:
    urls = []
    if file_hint:
        urls.append(file_hint)
    urls += [
        f"https://www.gutenberg.org/files/{ebook_id}/{ebook_id}-h/{ebook_id}-h.htm",
        f"https://www.gutenberg.org/cache/epub/{ebook_id}/pg{ebook_id}-images.html",
    ]
    dest = RAW / f"pg{ebook_id}.html"
    last = None
    for url in urls:
        try:
            fetch(url, dest)
            raw = dest.read_text(encoding="utf-8", errors="replace")
            if len(raw) > 1000:
                return html_to_text(pg_strip(raw))
        except Exception as err:  # noqa: BLE001
            last = err
            if dest.exists():
                dest.unlink()
    raise RuntimeError(f"gutenberg html {ebook_id}: {last}")


def slice_by_headings(text: str, headings: list[tuple[str, str, str]]) -> list[dict]:
    """headings: (id, locator, heading_regex_or_literal). Last slice runs to EOF."""
    lower = text
    spans: list[tuple[int, dict]] = []
    for sid, locator, heading in headings:
        # Prefer regex if it looks like one; else literal, case-insensitive
        try:
            m = re.search(heading, lower, re.I | re.M)
        except re.error:
            m = re.search(re.escape(heading), lower, re.I | re.M)
        if not m:
            continue
        spans.append((m.start(), {"id": sid, "locator": locator, "heading": sid}))
    spans.sort()
    sections = []
    for i, (start, meta) in enumerate(spans):
        end = spans[i + 1][0] if i + 1 < len(spans) else len(text)
        chunk = text[start:end]
        heading_line = chunk.split("\n", 1)[0].strip()
        paras = paragraphs(chunk)
        if paras:
            sections.append(section(meta["id"], meta["locator"], heading_line[:120], paras))
    return sections


def take_paras(paras: list[str], start: int, end: int | None = None) -> list[str]:
    return paras[start:end]


def first_match_index(paras: list[str], pattern: str) -> int:
    rx = re.compile(pattern, re.I)
    for i, p in enumerate(paras):
        if rx.search(p):
            return i
    return 0


# ---------------------------------------------------------------------------
# Per-work builders
# ---------------------------------------------------------------------------


def build_burnet() -> None:
    text = gutenberg_html(67097)
    dump_text(
        tid="burnet-early-greek",
        title="Early Greek Philosophy (selections)",
        author="John Burnet",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/67097",
        edition="John Burnet, Early Greek Philosophy, 3rd ed. (A. & C. Black); PG #67097",
        attribution="John Burnet, Early Greek Philosophy. Public domain. Source: Project Gutenberg #67097.",
        sections=slice_by_headings(
            text,
            [
                ("intro", "Introduction", r"\bINTRODUCTION\b"),
                ("milesians", "Chapter I. The Milesian School", r"CHAPTER I\b.*MILESIAN|THE MILESIAN SCHOOL"),
                ("science-religion", "Chapter II. Science and Religion", r"CHAPTER II\b.*SCIENCE AND RELIGION"),
                ("heraclitus", "Chapter III. Herakleitos of Ephesos", r"CHAPTER III\b.*HERAKLEITOS|HERAKLEITOS OF EPHESOS"),
                ("parmenides", "Chapter IV. Parmenides of Elea", r"CHAPTER IV\b.*PARMENIDES|PARMENIDES OF ELEA"),
                ("empedocles", "Chapter V. Empedokles of Akragas", r"CHAPTER V\b.*EMPEDOKLES|EMPEDOKLES OF AKRAGAS"),
                ("anaxagoras", "Chapter VI. Anaxagoras of Klazomenai", r"CHAPTER VI\b.*ANAXAGORAS"),
                ("eleatics", "Chapter VIII. The Younger Eleatics", r"CHAPTER VIII\b.*YOUNGER ELEATICS|THE YOUNGER ELEATICS"),
                ("atomists", "Chapter IX. Leukippos of Miletos", r"CHAPTER IX\b.*LEUKIPPOS|LEUKIPPOS OF MILETOS"),
            ],
        ),
    )


def _plato_dialogue(tid: str, title: str, ebook_id: int, locator: str) -> None:
    text = gutenberg_txt(ebook_id)
    # Drop Jowett's long introduction when present: start at the dialogue title or first "Socrates"
    m = re.search(rf"\n\s*{re.escape(title.upper())}\s*\n", text)
    if not m:
        m = re.search(r"\nPERSONS OF THE DIALOGUE", text, re.I)
    body = text[m.start() :] if m else text
    paras = paragraphs(body)
    # Keep the dialogue; drop trailing Gutenberg leftover if any
    dump_text(
        tid=tid,
        title=title,
        author="Plato",
        translator="Benjamin Jowett",
        source_name="Project Gutenberg",
        source_url=f"https://www.gutenberg.org/ebooks/{ebook_id}",
        edition=f"Jowett translation; Project Gutenberg EBook #{ebook_id}",
        sections=[section("full", locator, title, paras)],
    )


def build_republic() -> None:
    text = gutenberg_html(
        55201,
        "https://www.gutenberg.org/files/55201/55201-h/55201-h.htm",
    )
    secs = slice_by_headings(
        text,
        [
            ("book-i", "Republic Book I (Stephanus 327–354)", r"BOOK I\b"),
            ("book-ii", "Republic Book II (357–383)", r"BOOK II\b"),
            ("book-iv", "Republic Book IV (419–445)", r"BOOK IV\b"),
            ("book-vi", "Republic Book VI (484–511)", r"BOOK VI\b"),
            ("book-vii", "Republic Book VII (514–541)", r"BOOK VII\b"),
        ],
    )
    dump_text(
        tid="plato-republic",
        title="Republic (selections)",
        author="Plato",
        translator="Benjamin Jowett",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/55201",
        edition="Jowett, 3rd ed. with Stephanus numbers; PG #55201",
        sections=secs,
    )


def build_aristotle_categories() -> None:
    text = gutenberg_txt(2412)
    dump_text(
        tid="aristotle-categories",
        title="Categories (chs. 1–5)",
        author="Aristotle",
        translator="E. M. Edghill",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/2412",
        edition="Edghill; Project Gutenberg EBook #2412",
        sections=slice_by_headings(
            text,
            [
                ("cat-1", "Categories 1", r"Part 1\b"),
                ("cat-2", "Categories 2", r"Part 2\b"),
                ("cat-3", "Categories 3", r"Part 3\b"),
                ("cat-4", "Categories 4", r"Part 4\b"),
                ("cat-5", "Categories 5 (substance)", r"Part 5\b"),
            ],
        )[:5],
    )


def build_mit(tid: str, title: str, author: str, translator: str, url: str, edition: str, headings: list[tuple[str, str, str]]) -> None:
    dest = RAW / f"{tid}.txt"
    fetch(url, dest)
    text = dest.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"Provided by The Internet Classics Archive\..*?Available online at\s+\S+", "", text, flags=re.S)
    dump_text(
        tid=tid,
        title=title,
        author=author,
        translator=translator,
        source_name="Internet Classics Archive (MIT)",
        source_url=url.replace(".mb.txt", ".html"),
        edition=edition,
        sections=slice_by_headings(text, headings) or [section("full", title, title, paragraphs(text))],
    )


def build_epictetus() -> None:
    text = gutenberg_txt(45109)
    paras = paragraphs(text)
    # Manual is short; store whole body after the title
    dump_text(
        tid="epictetus-enchiridion",
        title="The Enchiridion",
        author="Epictetus",
        translator="Thomas W. Higginson (this PG edition)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/45109",
        edition="Project Gutenberg EBook #45109",
        sections=[section("full", "Enchiridion, complete", "The Enchiridion", paras)],
    )


def build_marcus() -> None:
    text = gutenberg_html(2680, "https://www.gutenberg.org/files/2680/2680-h/2680-h.htm")
    dump_text(
        tid="marcus-meditations",
        title="Meditations (Books II–IV)",
        author="Marcus Aurelius",
        translator="George Long",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/2680",
        edition="George Long; PG #2680",
        sections=slice_by_headings(
            text,
            [
                ("book-ii", "Book II", r"THE SECOND BOOK|BOOK II\b"),
                ("book-iii", "Book III", r"THE THIRD BOOK|BOOK III\b"),
                ("book-iv", "Book IV", r"THE FOURTH BOOK|BOOK IV\b"),
            ],
        ),
    )


def build_lucretius() -> None:
    text = gutenberg_html(785, "https://www.gutenberg.org/files/785/785-h/785-h.htm")
    dump_text(
        tid="lucretius-nature",
        title="Of the Nature of Things (Books I, III selections)",
        author="Lucretius",
        translator="William Ellery Leonard",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/785",
        edition="Leonard metrical translation; PG #785",
        sections=slice_by_headings(
            text,
            [
                ("book-i", "Book I", r"BOOK I\b"),
                ("book-iii", "Book III", r"BOOK III\b"),
            ],
        ),
    )


def build_sextus() -> None:
    text = gutenberg_html(17556)
    dump_text(
        tid="sextus-outlines",
        title="Pyrrhonic Sketches, Book I",
        author="Sextus Empiricus",
        translator="Mary Mills Patrick",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/17556",
        edition="Patrick, Sextus Empiricus and Greek Scepticism; PG #17556",
        sections=slice_by_headings(
            text,
            [
                ("book-i", "Pyrrhonic Sketches Book I", r"PYRRHONIC SKETCHES|BOOK I\b"),
            ],
        )
        or [section("book-i", "Book I", "Pyrrhonic Sketches", paragraphs(text)[-80:])],
    )


def build_augustine() -> None:
    text = gutenberg_html(3296, "https://www.gutenberg.org/files/3296/3296-h/3296-h.htm")
    dump_text(
        tid="augustine-confessions",
        title="Confessions (Books VII, VIII, XI)",
        author="Augustine of Hippo",
        translator="E. B. Pusey",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/3296",
        edition="Pusey; PG #3296",
        sections=slice_by_headings(
            text,
            [
                ("book-vii", "Book VII", r"^BOOK VII\b|## BOOK VII"),
                ("book-viii", "Book VIII", r"^BOOK VIII\b|## BOOK VIII"),
                ("book-xi", "Book XI", r"^BOOK XI\b|## BOOK XI"),
            ],
        ),
    )


def build_boethius() -> None:
    text = gutenberg_html(14328, "https://www.gutenberg.org/files/14328/14328-h/14328-h.htm")
    dump_text(
        tid="boethius-consolation",
        title="The Consolation of Philosophy (Books I, III)",
        author="Boethius",
        translator="H. R. James",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/14328",
        edition="H. R. James; PG #14328",
        sections=slice_by_headings(
            text,
            [
                ("book-i", "Book I", r"BOOK I\b"),
                ("book-iii", "Book III", r"BOOK III\b"),
            ],
        ),
    )


def build_anselm() -> None:
    url = "https://www.ccel.org/ccel/anselm/basic_works.all.html"
    dest = RAW / "anselm.html"
    fetch(url, dest)
    text = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
    dump_text(
        tid="anselm-proslogion",
        title="Proslogium, with Gaunilo’s reply and Anselm’s rejoinder",
        author="Anselm of Canterbury",
        translator="Sidney Norton Deane",
        source_name="Christian Classics Ethereal Library",
        source_url="https://www.ccel.org/ccel/anselm/basic_works.html",
        edition="Deane, Open Court 1903/1926; CCEL",
        sections=slice_by_headings(
            text,
            [
                ("proslogium", "Proslogium", r"PROSLOGIUM\b"),
                ("gaunilo", "Gaunilo, In Behalf of the Fool", r"IN BEHALF OF THE FOOL|GAUNILO"),
                ("reply", "Anselm’s reply to Gaunilo", r"ANSELM.?S APOLOGETIC|REPLY ON BEHALF"),
            ],
        ),
    )


def build_aquinas() -> None:
    pages = [
        ("st-i-q1", "Summa theologiae I, q.1", "https://www.newadvent.org/summa/1001.htm", "Sacred doctrine"),
        ("st-i-q2", "Summa theologiae I, q.2", "https://www.newadvent.org/summa/1002.htm", "The existence of God (Five Ways)"),
        ("st-i-ii-q90", "Summa theologiae I–II, q.90", "https://www.newadvent.org/summa/2090.htm", "The essence of law"),
        ("st-i-ii-q94", "Summa theologiae I–II, q.94", "https://www.newadvent.org/summa/2094.htm", "The natural law"),
    ]
    sections = []
    for sid, locator, url, heading in pages:
        dest = RAW / f"{sid}.html"
        fetch(url, dest)
        text = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
        # Cut New Advent chrome: keep from Article 1
        m = re.search(r"Article\s+1\b", text)
        body = text[m.start() :] if m else text
        # drop "Continue to" navigation
        body = re.split(r"Continue to\b", body)[0]
        sections.append(section(sid, locator, heading, paragraphs(body)))
    dump_text(
        tid="aquinas-summa",
        title="Summa theologiae (selected questions)",
        author="Thomas Aquinas",
        translator="Fathers of the English Dominican Province",
        source_name="New Advent",
        source_url="https://www.newadvent.org/summa/",
        edition="English Dominican Province (1911–25); hosted at New Advent",
        sections=sections,
    )


def build_averroes() -> None:
    text = gutenberg_html(65708)
    dump_text(
        tid="averroes-decisive",
        title="A Decisive Discourse on the Relation between Religion and Philosophy",
        author="Averroes (Ibn Rushd)",
        translator="Mohammad Jamil-ur-Rehman",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/65708",
        edition="The Philosophy and Theology of Averroes; PG #65708",
        sections=slice_by_headings(
            text,
            [
                ("decisive", "Decisive Discourse", r"DECISIVE DISCOURSE|DELINEATION OF THE RELATION"),
            ],
        )
        or [section("decisive", "Decisive Discourse", "Decisive Discourse", paragraphs(text)[:80])],
    )


def build_maimonides() -> None:
    text = gutenberg_html(73584, "https://www.gutenberg.org/files/73584/73584-h/73584-h.htm")
    dump_text(
        tid="maimonides-guide",
        title="The Guide for the Perplexed (introduction and I.50–52)",
        author="Moses Maimonides",
        translator="M. Friedländer",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/73584",
        edition="Friedländer, 2nd ed.; PG #73584",
        sections=slice_by_headings(
            text,
            [
                ("intro", "Introduction", r"THE OBJECT OF THE GUIDE|INTRODUCTION"),
                ("i-50", "Part I, ch. 50", r"CHAPTER L\b|CHAPTER 50\b"),
                ("i-51", "Part I, ch. 51", r"CHAPTER LI\b|CHAPTER 51\b"),
                ("i-52", "Part I, ch. 52", r"CHAPTER LII\b|CHAPTER 52\b"),
            ],
        ),
    )


def build_bacon() -> None:
    text = gutenberg_html(45988, "https://www.gutenberg.org/files/45988/45988-h/45988-h.htm")
    dump_text(
        tid="bacon-novum-organum",
        title="Novum Organum, Book I (selected aphorisms)",
        author="Francis Bacon",
        translator="n/a (English edition of the Latin)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/45988",
        edition="PG #45988",
        sections=slice_by_headings(
            text,
            [
                ("book-i", "Book I, Aphorisms", r"APHORISMS.?BOOK I|BOOK I\b"),
            ],
        ),
    )


def build_descartes_discourse() -> None:
    text = gutenberg_html(59, "https://www.gutenberg.org/files/59/59-h/59-h.htm")
    dump_text(
        tid="descartes-discourse",
        title="Discourse on the Method (Parts I–IV)",
        author="René Descartes",
        translator="John Veitch",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/59",
        edition="Veitch; PG #59",
        sections=slice_by_headings(
            text,
            [
                ("part-1", "Part I", r"PART I\b"),
                ("part-2", "Part II", r"PART II\b"),
                ("part-3", "Part III", r"PART III\b"),
                ("part-4", "Part IV", r"PART IV\b"),
            ],
        ),
    )


def build_descartes_meditations() -> None:
    text = gutenberg_html(70091, "https://www.gutenberg.org/files/70091/70091-h/70091-h.htm")
    dump_text(
        tid="descartes-meditations",
        title="Meditations on First Philosophy",
        author="René Descartes",
        translator="William Molyneux (1680)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/70091",
        edition="Molyneux, Six Metaphysical Meditations; PG #70091",
        sections=slice_by_headings(
            text,
            [
                ("med-1", "Meditation I", r"Meditat\.?\s*I\b|Meditation 1\b|Of Things Doubtful"),
                ("med-2", "Meditation II", r"Meditat\.?\s*II\b|Meditation 2\b|Of the Nature of Mans Mind"),
                ("med-3", "Meditation III", r"Meditat\.?\s*III\b|Meditation 3\b|Of GOD"),
                ("med-4", "Meditation IV", r"Meditat\.?\s*IV\b|Meditation 4\b|Of Truth and Falshood"),
                ("med-5", "Meditation V", r"Meditat\.?\s*V\b|Meditation 5\b|Of the Essence of Things Material"),
                ("med-6", "Meditation VI", r"Meditat\.?\s*VI\b|Meditation 6\b|Of Corporeal Beings"),
            ],
        ),
    )


def build_spinoza() -> None:
    text = gutenberg_html(3800, "https://www.gutenberg.org/files/3800/3800-h/3800-h.htm")
    dump_text(
        tid="spinoza-ethics",
        title="Ethics, Part I (and Part IV preface / selected propositions)",
        author="Benedict de Spinoza",
        translator="R. H. M. Elwes",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/3800",
        edition="Elwes; PG #3800",
        sections=slice_by_headings(
            text,
            [
                ("part-i", "Part I. Concerning God", r"PART I\b.*GOD|CONCERNING GOD"),
                ("part-iv", "Part IV. Of Human Bondage", r"PART IV\b|OF HUMAN BONDAGE"),
            ],
        ),
    )


def build_pascal() -> None:
    text = gutenberg_html(18269, "https://www.gutenberg.org/files/18269/18269-h/18269-h.htm")
    paras = paragraphs(text)
    # Keep a manageable stretch around the wager / misery of man if we can find it
    idx = first_match_index(paras, r"infinite nothing|wager|you must wager")
    start = max(0, idx - 8)
    dump_text(
        tid="pascal-pensees",
        title="Pensées (selection: wretchedness, diversion, wager)",
        author="Blaise Pascal",
        translator="W. F. Trotter",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/18269",
        edition="Trotter; PG #18269",
        sections=[section("wager", "Pensées (Trotter numbering; wager cluster)", "Wretchedness, diversion, and the wager", paras[start : start + 40])],
    )


def build_leibniz() -> None:
    url = "https://en.wikisource.org/wiki/Monadology_(Leibniz,_tr._Latta)"
    dest = RAW / "monadology.html"
    fetch(url, dest)
    text = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
    dump_text(
        tid="leibniz-monadology",
        title="The Monadology",
        author="G. W. Leibniz",
        translator="Robert Latta",
        source_name="Wikisource",
        source_url=url,
        edition="Latta 1898, via Wikisource",
        sections=[section("full", "Monadology, §§1–90", "The Monadology", paragraphs(text))],
    )


def build_hobbes() -> None:
    text = gutenberg_html(3207, "https://www.gutenberg.org/files/3207/3207-h/3207-h.htm")
    dump_text(
        tid="hobbes-leviathan",
        title="Leviathan (chs. 13–14, 17–21)",
        author="Thomas Hobbes",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/3207",
        edition="1651 text; PG #3207",
        attribution="Thomas Hobbes, Leviathan (1651). Public domain. Source: Project Gutenberg #3207.",
        sections=slice_by_headings(
            text,
            [
                ("ch-13", "Chapter XIII", r"CHAPTER XIII\b"),
                ("ch-14", "Chapter XIV", r"CHAPTER XIV\b"),
                ("ch-17", "Chapter XVII", r"CHAPTER XVII\b"),
                ("ch-18", "Chapter XVIII", r"CHAPTER XVIII\b"),
                ("ch-21", "Chapter XXI", r"CHAPTER XXI\b"),
            ],
        ),
    )


def build_locke_essay() -> None:
    text = gutenberg_html(10615, "https://www.gutenberg.org/files/10615/10615-h/10615-h.htm")
    dump_text(
        tid="locke-essay",
        title="An Essay Concerning Human Understanding (selections)",
        author="John Locke",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/10615",
        edition="2nd ed. text, Books I–II; PG #10615",
        attribution="John Locke, An Essay Concerning Human Understanding. Public domain. Source: Project Gutenberg #10615.",
        sections=slice_by_headings(
            text,
            [
                ("i-1", "Book I, ch. 1", r"CHAPTER I\.\s*INTRODUCTION"),
                ("i-2", "Book I, ch. 2", r"CHAPTER II\.\s*NO INNATE SPECULATIVE"),
                ("ii-1", "Book II, ch. 1", r"CHAPTER I\.\s*OF IDEAS IN GENERAL|BOOK II"),
                ("ii-8", "Book II, ch. 8", r"CHAPTER VIII\b"),
                ("ii-27", "Book II, ch. 27", r"CHAPTER XXVII\b"),
            ],
        ),
    )


def build_locke_treatise() -> None:
    text = gutenberg_html(7370, "https://www.gutenberg.org/files/7370/7370-h/7370-h.htm")
    dump_text(
        tid="locke-second-treatise",
        title="Second Treatise of Government (chs. 1–5, 8–9, 19)",
        author="John Locke",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/7370",
        edition="1690 text; PG #7370",
        attribution="John Locke, Second Treatise of Government (1690). Public domain. Source: Project Gutenberg #7370.",
        sections=slice_by_headings(
            text,
            [
                ("ch-1", "Chapter I", r"CHAPTER\.?\s*I\b"),
                ("ch-2", "Chapter II. Of the State of Nature", r"CHAPTER\.?\s*II\b"),
                ("ch-5", "Chapter V. Of Property", r"CHAPTER\.?\s*V\b"),
                ("ch-8", "Chapter VIII", r"CHAPTER\.?\s*VIII\b"),
                ("ch-9", "Chapter IX", r"CHAPTER\.?\s*IX\b"),
                ("ch-19", "Chapter XIX", r"CHAPTER\.?\s*XIX\b"),
            ],
        ),
    )


def build_berkeley() -> None:
    text = gutenberg_html(4723, "https://www.gutenberg.org/files/4723/4723-h/4723-h.htm")
    paras = paragraphs(text)
    dump_text(
        tid="berkeley-principles",
        title="A Treatise Concerning the Principles of Human Knowledge (Introduction and §§1–33)",
        author="George Berkeley",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/4723",
        edition="PG #4723",
        attribution="George Berkeley, Principles of Human Knowledge. Public domain. Source: Project Gutenberg #4723.",
        sections=[
            section("intro-main", "Introduction + opening principles (§§1–33 approx.)", "Principles of Human Knowledge", paras[:90]),
        ],
    )


def build_hume_enquiry() -> None:
    text = gutenberg_html(9662, "https://www.gutenberg.org/files/9662/9662-h/9662-h.htm")
    dump_text(
        tid="hume-enquiry",
        title="An Enquiry Concerning Human Understanding",
        author="David Hume",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/9662",
        edition="PG #9662",
        attribution="David Hume, An Enquiry Concerning Human Understanding. Public domain. Source: Project Gutenberg #9662.",
        sections=slice_by_headings(
            text,
            [
                ("sec-2", "Section II", r"SECTION II\b|OF THE ORIGIN OF IDEAS"),
                ("sec-3", "Section III", r"SECTION III\b"),
                ("sec-4", "Section IV", r"SECTION IV\b|SCEPTICAL DOUBTS"),
                ("sec-5", "Section V", r"SECTION V\b|SCEPTICAL SOLUTION"),
                ("sec-7", "Section VII", r"SECTION VII\b|OF THE IDEA OF NECESSARY CONNEXION"),
                ("sec-8", "Section VIII", r"SECTION VIII\b|OF LIBERTY AND NECESSITY"),
                ("sec-10", "Section X", r"SECTION X\b|OF MIRACLES"),
                ("sec-12", "Section XII", r"SECTION XII\b|OF THE ACADEMICAL"),
            ],
        ),
    )


def build_hume_treatise() -> None:
    text = gutenberg_html(4705, "https://www.gutenberg.org/files/4705/4705-h/4705-h.htm")
    dump_text(
        tid="hume-treatise",
        title="A Treatise of Human Nature I.4.6 (personal identity)",
        author="David Hume",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/4705",
        edition="PG #4705",
        attribution="David Hume, A Treatise of Human Nature. Public domain. Source: Project Gutenberg #4705.",
        sections=slice_by_headings(
            text,
            [
                ("i-4-6", "Book I, Part 4, Section 6", r"OF PERSONAL IDENTITY"),
            ],
        ),
    )


def build_hume_dialogues() -> None:
    text = gutenberg_html(4583)
    dump_text(
        tid="hume-dialogues",
        title="Dialogues Concerning Natural Religion (Parts II, X–XI)",
        author="David Hume",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/4583",
        edition="PG #4583",
        attribution="David Hume, Dialogues Concerning Natural Religion. Public domain. Source: Project Gutenberg #4583.",
        sections=slice_by_headings(
            text,
            [
                ("part-2", "Part II", r"PART II\b"),
                ("part-10", "Part X", r"PART X\b"),
                ("part-11", "Part XI", r"PART XI\b"),
            ],
        ),
    )


def build_rousseau() -> None:
    text = gutenberg_html(46333)
    dump_text(
        tid="rousseau-contract-discourses",
        title="Discourse on Inequality and The Social Contract (selections)",
        author="Jean-Jacques Rousseau",
        translator="G. D. H. Cole",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/46333",
        edition="Cole, Everyman; PG #46333",
        sections=slice_by_headings(
            text,
            [
                ("inequality-1", "Discourse on Inequality, Part I", r"FIRST PART\b|DISCOURSE ON THE ORIGIN"),
                ("contract-i", "Social Contract, Book I", r"BOOK I\b"),
                ("contract-ii", "Social Contract, Book II", r"BOOK II\b"),
            ],
        ),
    )


def build_smith() -> None:
    text = gutenberg_html(67363, "https://www.gutenberg.org/files/67363/67363-h/67363-h.htm")
    dump_text(
        tid="smith-tms",
        title="The Theory of Moral Sentiments I.i",
        author="Adam Smith",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/67363",
        edition="PG #67363",
        attribution="Adam Smith, The Theory of Moral Sentiments. Public domain. Source: Project Gutenberg #67363.",
        sections=slice_by_headings(
            text,
            [
                ("i-i", "Part I, Section I", r"PART I\b|OF THE PROPRIETY OF ACTION"),
            ],
        ),
    )


def build_kant_cpr() -> None:
    text = gutenberg_html(4280, "https://www.gutenberg.org/files/4280/4280-h/4280-h.htm")
    dump_text(
        tid="kant-cpr",
        title="Critique of Pure Reason (Prefaces and Transcendental Aesthetic)",
        author="Immanuel Kant",
        translator="J. M. D. Meiklejohn",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/4280",
        edition="Meiklejohn; PG #4280",
        sections=slice_by_headings(
            text,
            [
                ("preface-a", "Preface to the first edition (A)", r"PREFACE TO THE FIRST EDITION"),
                ("preface-b", "Preface to the second edition (B)", r"PREFACE TO THE SECOND EDITION"),
                ("intro", "Introduction", r"^INTRODUCTION\b"),
                ("aesthetic", "Transcendental Aesthetic", r"TRANSCENDENTAL AESTHETIC"),
                ("logic-open", "Opening of Transcendental Logic / Analytic", r"TRANSCENDENTAL LOGIC|TRANSCENDENTAL ANALYTIC"),
            ],
        ),
    )


def build_kant_groundwork() -> None:
    text = gutenberg_html(5682, "https://www.gutenberg.org/files/5682/5682-h/5682-h.htm")
    dump_text(
        tid="kant-groundwork",
        title="Fundamental Principles of the Metaphysic of Morals",
        author="Immanuel Kant",
        translator="Thomas Kingsmill Abbott",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/5682",
        edition="Abbott; PG #5682",
        sections=slice_by_headings(
            text,
            [
                ("preface", "Preface", r"^PREFACE\b"),
                ("sec-1", "First Section", r"FIRST SECTION"),
                ("sec-2", "Second Section", r"SECOND SECTION"),
                ("sec-3", "Third Section", r"THIRD SECTION"),
            ],
        ),
    )


def build_hegel() -> None:
    url = "https://www.marxists.org/reference/archive/hegel/works/ph/phba.htm"
    # Lordship and bondage lives under self-consciousness
    url2 = "https://www.marxists.org/reference/archive/hegel/works/ph/phselfc.htm"
    dest1 = RAW / "hegel-preface.html"
    dest2 = RAW / "hegel-selfc.html"
    fetch(url, dest1)
    fetch(url2, dest2)
    t1 = html_to_text(dest1.read_text(encoding="utf-8", errors="replace"))
    t2 = html_to_text(dest2.read_text(encoding="utf-8", errors="replace"))
    dump_text(
        tid="hegel-phenomenology",
        title="Phenomenology of Spirit (Preface excerpt; Lordship and Bondage)",
        author="G. W. F. Hegel",
        translator="J. B. Baillie",
        source_name="Marxists Internet Archive (Baillie 1910)",
        source_url="https://www.marxists.org/reference/archive/hegel/phindex.htm",
        edition="Baillie 1910 translation of the 1807 Phenomenology",
        sections=[
            section("preface", "Preface (opening)", "Preface", paragraphs(t1)[:35]),
            section("lordship", "B. Self-Consciousness: Lordship and Bondage", "Lordship and Bondage", paragraphs(t2)),
        ],
    )


def build_schopenhauer() -> None:
    text = gutenberg_html(38427, "https://www.gutenberg.org/files/38427/38427-h/38427-h.html")
    dump_text(
        tid="schopenhauer-will",
        title="The World as Will and Idea (opening of Books I–II)",
        author="Arthur Schopenhauer",
        translator="R. B. Haldane and J. Kemp",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/38427",
        edition="Haldane & Kemp, vol. 1; PG #38427",
        sections=slice_by_headings(
            text,
            [
                ("book-i", "First Book. The World as Idea", r"FIRST BOOK\b|THE WORLD AS IDEA"),
                ("book-ii", "Second Book. The World as Will", r"SECOND BOOK\b|THE WORLD AS WILL"),
            ],
        ),
    )


def build_mill_liberty() -> None:
    text = gutenberg_html(34901, "https://www.gutenberg.org/files/34901/34901-h/34901-h.htm")
    dump_text(
        tid="mill-on-liberty",
        title="On Liberty (chs. I–III)",
        author="John Stuart Mill",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/34901",
        edition="PG #34901",
        attribution="John Stuart Mill, On Liberty. Public domain. Source: Project Gutenberg #34901.",
        sections=slice_by_headings(
            text,
            [
                ("ch-1", "Chapter I", r"CHAPTER I\b"),
                ("ch-2", "Chapter II", r"CHAPTER II\b"),
                ("ch-3", "Chapter III", r"CHAPTER III\b"),
            ],
        ),
    )


def build_mill_util() -> None:
    text = gutenberg_html(11224, "https://www.gutenberg.org/files/11224/11224-h/11224-h.htm")
    dump_text(
        tid="mill-utilitarianism",
        title="Utilitarianism (chs. I–II)",
        author="John Stuart Mill",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/11224",
        edition="PG #11224",
        attribution="John Stuart Mill, Utilitarianism. Public domain. Source: Project Gutenberg #11224.",
        sections=slice_by_headings(
            text,
            [
                ("ch-1", "Chapter I", r"CHAPTER I\b|GENERAL REMARKS"),
                ("ch-2", "Chapter II", r"CHAPTER II\b|WHAT UTILITARIANISM IS"),
            ],
        ),
    )


def build_kierkegaard() -> None:
    text = gutenberg_html(60333, "https://www.gutenberg.org/files/60333/60333-h/60333-h.htm")
    dump_text(
        tid="kierkegaard-selections",
        title="Fear and Trembling (Hollander selection)",
        author="Søren Kierkegaard",
        translator="L. M. Hollander",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/60333",
        edition="Selections from the Writings of Kierkegaard, University of Texas 1923; PG #60333",
        sections=slice_by_headings(
            text,
            [
                ("fear", "Fear and Trembling", r"FEAR AND TREMBLING"),
            ],
        ),
    )


def build_marx() -> None:
    text = gutenberg_html(61, "https://www.gutenberg.org/files/61/61-h/61-h.htm")
    dump_text(
        tid="marx-manifesto",
        title="The Communist Manifesto",
        author="Karl Marx and Friedrich Engels",
        translator="Samuel Moore (1888, with Engels)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/61",
        edition="Moore/Engels 1888 English; PG #61",
        sections=slice_by_headings(
            text,
            [
                ("i", "I. Bourgeois and Proletarians", r"I\.\s*BOURGEOIS AND PROLETARIANS"),
                ("ii", "II. Proletarians and Communists", r"II\.\s*PROLETARIANS AND COMMUNISTS"),
            ],
        ),
    )


def build_nietzsche_genealogy() -> None:
    text = gutenberg_html(52319, "https://www.gutenberg.org/files/52319/52319-h/52319-h.htm")
    dump_text(
        tid="nietzsche-genealogy",
        title="The Genealogy of Morals (Preface and Essays I–II)",
        author="Friedrich Nietzsche",
        translator="Horace B. Samuel",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/52319",
        edition="Samuel; PG #52319",
        sections=slice_by_headings(
            text,
            [
                ("preface", "Preface", r"^PREFACE\b"),
                ("essay-i", "First Essay", r"FIRST ESSAY|GOOD AND EVIL"),
                ("essay-ii", "Second Essay", r"SECOND ESSAY|GUILT"),
            ],
        ),
    )


def build_nietzsche_gs() -> None:
    text = gutenberg_html(52124)
    paras = paragraphs(text)
    dump_text(
        tid="nietzsche-gay-science",
        title="The Joyful Wisdom (selected aphorisms)",
        author="Friedrich Nietzsche",
        translator="Thomas Common / Paul V. Cohn",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/52124",
        edition="Levy Complete Works vol. 10; PG #52124",
        sections=[section("selected", "Aphorisms including 125, 341 (Common numbering)", "The Joyful Wisdom (selection)", paras)],
    )


def build_peirce() -> None:
    url = "https://en.wikisource.org/wiki/How_to_Make_Our_Ideas_Clear"
    dest = RAW / "peirce.html"
    fetch(url, dest)
    text = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
    dump_text(
        tid="peirce-ideas-clear",
        title="How to Make Our Ideas Clear",
        author="Charles Sanders Peirce",
        translator="n/a (English original)",
        source_name="Wikisource",
        source_url=url,
        edition="Popular Science Monthly 12 (January 1878)",
        attribution="C. S. Peirce, How to Make Our Ideas Clear (1878). Public domain. Source: Wikisource.",
        sections=[section("full", "Complete essay (1878)", "How to Make Our Ideas Clear", paragraphs(text))],
    )


def build_james_pragmatism() -> None:
    text = gutenberg_html(5116, "https://www.gutenberg.org/files/5116/5116-h/5116-h.htm")
    dump_text(
        tid="james-pragmatism",
        title="Pragmatism (Lectures I–II)",
        author="William James",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/5116",
        edition="PG #5116",
        attribution="William James, Pragmatism. Public domain. Source: Project Gutenberg #5116.",
        sections=slice_by_headings(
            text,
            [
                ("lec-1", "Lecture I", r"LECTURE I\b"),
                ("lec-2", "Lecture II", r"LECTURE II\b"),
            ],
        ),
    )


def build_james_will() -> None:
    text = gutenberg_html(26659)
    dump_text(
        tid="james-will-to-believe",
        title="The Will to Believe",
        author="William James",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/26659",
        edition="PG #26659",
        attribution="William James, The Will to Believe. Public domain. Source: Project Gutenberg #26659.",
        sections=slice_by_headings(
            text,
            [
                ("essay", "The Will to Believe", r"THE WILL TO BELIEVE"),
            ],
        )
        or [section("essay", "The Will to Believe", "The Will to Believe", paragraphs(text)[:60])],
    )


def build_dewey() -> None:
    text = gutenberg_html(40089)
    dump_text(
        tid="dewey-reconstruction",
        title="Reconstruction in Philosophy (chs. I–II)",
        author="John Dewey",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/40089",
        edition="1920; PG #40089",
        attribution="John Dewey, Reconstruction in Philosophy (1920). Public domain. Source: Project Gutenberg #40089.",
        sections=slice_by_headings(
            text,
            [
                ("ch-1", "Chapter I", r"CHAPTER I\b"),
                ("ch-2", "Chapter II", r"CHAPTER II\b"),
            ],
        ),
    )


def build_dubois() -> None:
    text = gutenberg_html(408, "https://www.gutenberg.org/files/408/408-h/408-h.htm")
    dump_text(
        tid="dubois-souls",
        title="The Souls of Black Folk (ch. I)",
        author="W. E. B. Du Bois",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/408",
        edition="1903; PG #408",
        attribution="W. E. B. Du Bois, The Souls of Black Folk (1903). Public domain. Source: Project Gutenberg #408.",
        sections=slice_by_headings(
            text,
            [
                ("ch-1", "Chapter I. Of Our Spiritual Strivings", r"OF OUR SPIRITUAL STRIVINGS"),
            ],
        ),
    )


def build_moore() -> None:
    text = gutenberg_html(53430, "https://www.gutenberg.org/files/53430/53430-h/53430-h.htm")
    dump_text(
        tid="moore-principia-ethica",
        title="Principia Ethica (ch. I)",
        author="G. E. Moore",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/53430",
        edition="1903; PG #53430",
        attribution="G. E. Moore, Principia Ethica (1903). Public domain. Source: Project Gutenberg #53430.",
        sections=slice_by_headings(
            text,
            [
                ("ch-1", "Chapter I. The Subject-Matter of Ethics", r"CHAPTER I\b|THE SUBJECT-MATTER OF ETHICS"),
            ],
        ),
    )


def build_russell() -> None:
    text = gutenberg_html(5827, "https://www.gutenberg.org/files/5827/5827-h/5827-h.htm")
    dump_text(
        tid="russell-problems",
        title="The Problems of Philosophy (chs. I, V, VI, XV)",
        author="Bertrand Russell",
        translator="n/a (English original)",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/5827",
        edition="1912; PG #5827",
        attribution="Bertrand Russell, The Problems of Philosophy (1912). Public domain. Source: Project Gutenberg #5827.",
        sections=slice_by_headings(
            text,
            [
                ("ch-1", "Chapter I. Appearance and Reality", r"CHAPTER I\b.*APPEARANCE"),
                ("ch-5", "Chapter V. Knowledge by Acquaintance and Description", r"CHAPTER V\b"),
                ("ch-6", "Chapter VI. On Induction", r"CHAPTER VI\b"),
                ("ch-15", "Chapter XV. The Value of Philosophy", r"CHAPTER XV\b"),
            ],
        ),
    )


def build_tractatus() -> None:
    # Prefer HTML/plain if present; else txt
    try:
        text = gutenberg_html(5740)
    except Exception:
        text = gutenberg_txt(5740)
    dump_text(
        tid="wittgenstein-tractatus",
        title="Tractatus Logico-Philosophicus",
        author="Ludwig Wittgenstein",
        translator="C. K. Ogden",
        source_name="Project Gutenberg",
        source_url="https://www.gutenberg.org/ebooks/5740",
        edition="Ogden, 1922, with Russell’s introduction; PG #5740",
        sections=slice_by_headings(
            text,
            [
                ("p1", "Propositions 1–1.21", r"^1\s+The world is everything"),
                ("p2", "Propositions 2–", r"^2\s+What is the case"),
                ("p4", "Propositions 4–", r"^4\s+The thought is"),
                ("p6", "Propositions 6–7", r"^6\s+The general form"),
                ("p7", "Proposition 7", r"^7\s+Whereof one cannot speak"),
            ],
        )
        or [section("full", "Tractatus (Ogden)", "Tractatus Logico-Philosophicus", paragraphs(text))],
    )


def build_plotinus() -> None:
    url = "https://www.ccel.org/ccel/plotinus/enneads.html"
    dest = RAW / "plotinus.html"
    fetch(url, dest)
    text = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
    dump_text(
        tid="plotinus-enneads",
        title="The Enneads (V.1 and VI.9)",
        author="Plotinus",
        translator="Stephen MacKenna and B. S. Page",
        source_name="Christian Classics Ethereal Library",
        source_url=url,
        edition="MacKenna/Page; CCEL",
        sections=slice_by_headings(
            text,
            [
                ("v-1", "Ennead V.1 The Three Initial Hypostases", r"THREE INITIAL HYPOSTASES|FIFTH ENNEAD.*FIRST"),
                ("vi-9", "Ennead VI.9 On the Good, or the One", r"ON THE GOOD, OR THE ONE|SIXTH ENNEAD.*NINTH"),
            ],
        )
        or [section("selected", "Enneads (MacKenna)", "The Enneads", paragraphs(text)[:70])],
    )


def build_epicurus() -> None:
    url = "https://classics.mit.edu/Epicurus/menoec.mb.txt"
    dest = RAW / "epicurus-menoeceus.txt"
    fetch(url, dest)
    text = dest.read_text(encoding="utf-8", errors="replace")
    dump_text(
        tid="epicurus-menoeceus",
        title="Letter to Menoeceus",
        author="Epicurus",
        translator="Robert Drew Hicks",
        source_name="Internet Classics Archive (MIT)",
        source_url="https://classics.mit.edu/Epicurus/menoec.html",
        edition="Hicks, via MIT Classics",
        sections=[section("full", "Complete letter", "Letter to Menoeceus", paragraphs(text))],
    )


def build_aristotle_ne() -> None:
    build_mit(
        "aristotle-nicomachean-ethics",
        "Nicomachean Ethics (Books I–II, X.6–8)",
        "Aristotle",
        "W. D. Ross",
        "https://classics.mit.edu/Aristotle/nicomachaen.mb.txt",
        "Ross, via MIT Classics",
        [
            ("ne-i", "Book I", r"BOOK I\b"),
            ("ne-ii", "Book II", r"BOOK II\b"),
            ("ne-x", "Book X", r"BOOK X\b"),
        ],
    )


def build_aristotle_physics() -> None:
    build_mit(
        "aristotle-physics",
        "Physics (Book II.1–3)",
        "Aristotle",
        "R. P. Hardie and R. K. Gaye",
        "https://classics.mit.edu/Aristotle/physics.mb.txt",
        "Hardie & Gaye, via MIT Classics",
        [
            ("phys-ii", "Book II", r"BOOK II\b"),
        ],
    )


def build_aristotle_metaphysics() -> None:
    build_mit(
        "aristotle-metaphysics",
        "Metaphysics (I.1–2; IV.1–2)",
        "Aristotle",
        "W. D. Ross",
        "https://classics.mit.edu/Aristotle/metaphysics.mb.txt",
        "Ross, via MIT Classics",
        [
            ("met-i", "Book I (Alpha)", r"BOOK I\b"),
            ("met-iv", "Book IV (Gamma)", r"BOOK IV\b"),
        ],
    )


def build_aristotle_post() -> None:
    build_mit(
        "aristotle-posterior-analytics",
        "Posterior Analytics I.1–3",
        "Aristotle",
        "G. R. G. Mure",
        "https://classics.mit.edu/Aristotle/posteri.mb.txt",
        "Mure, via MIT Classics",
        [
            ("pa-i", "Book I", r"BOOK I\b"),
        ],
    )


BUILDERS = [
    ("burnet-early-greek", build_burnet),
    ("plato-euthyphro", lambda: _plato_dialogue("plato-euthyphro", "Euthyphro", 1642, "Stephanus 2a–16a")),
    ("plato-apology", lambda: _plato_dialogue("plato-apology", "Apology", 1656, "Stephanus 17a–42a")),
    ("plato-crito", lambda: _plato_dialogue("plato-crito", "Crito", 1657, "Stephanus 43a–54e")),
    ("plato-meno", lambda: _plato_dialogue("plato-meno", "Meno", 1643, "Stephanus 70a–100b")),
    ("plato-republic", build_republic),
    ("aristotle-categories", build_aristotle_categories),
    ("aristotle-nicomachean-ethics", build_aristotle_ne),
    ("aristotle-physics", build_aristotle_physics),
    ("aristotle-metaphysics", build_aristotle_metaphysics),
    ("aristotle-posterior-analytics", build_aristotle_post),
    ("epicurus-menoeceus", build_epicurus),
    ("lucretius-nature", build_lucretius),
    ("epictetus-enchiridion", build_epictetus),
    ("marcus-meditations", build_marcus),
    ("sextus-outlines", build_sextus),
    ("plotinus-enneads", build_plotinus),
    ("boethius-consolation", build_boethius),
    ("augustine-confessions", build_augustine),
    ("anselm-proslogion", build_anselm),
    ("aquinas-summa", build_aquinas),
    ("averroes-decisive", build_averroes),
    ("maimonides-guide", build_maimonides),
    ("bacon-novum-organum", build_bacon),
    ("descartes-discourse", build_descartes_discourse),
    ("descartes-meditations", build_descartes_meditations),
    ("spinoza-ethics", build_spinoza),
    ("pascal-pensees", build_pascal),
    ("leibniz-monadology", build_leibniz),
    ("hobbes-leviathan", build_hobbes),
    ("locke-essay", build_locke_essay),
    ("locke-second-treatise", build_locke_treatise),
    ("berkeley-principles", build_berkeley),
    ("hume-enquiry", build_hume_enquiry),
    ("hume-treatise", build_hume_treatise),
    ("hume-dialogues", build_hume_dialogues),
    ("rousseau-contract-discourses", build_rousseau),
    ("smith-tms", build_smith),
    ("kant-cpr", build_kant_cpr),
    ("kant-groundwork", build_kant_groundwork),
    ("hegel-phenomenology", build_hegel),
    ("schopenhauer-will", build_schopenhauer),
    ("mill-on-liberty", build_mill_liberty),
    ("mill-utilitarianism", build_mill_util),
    ("kierkegaard-selections", build_kierkegaard),
    ("marx-manifesto", build_marx),
    ("nietzsche-genealogy", build_nietzsche_genealogy),
    ("nietzsche-gay-science", build_nietzsche_gs),
    ("peirce-ideas-clear", build_peirce),
    ("james-pragmatism", build_james_pragmatism),
    ("james-will-to-believe", build_james_will),
    ("dewey-reconstruction", build_dewey),
    ("dubois-souls", build_dubois),
    ("moore-principia-ethica", build_moore),
    ("russell-problems", build_russell),
    ("wittgenstein-tractatus", build_tractatus),
]


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    TEXTS.mkdir(parents=True, exist_ok=True)
    ok, failed = [], []
    for name, fn in BUILDERS:
        out = TEXTS / f"{name}.json"
        try:
            print(f"INGEST {name} ...", flush=True)
            fn()
            data = json.loads(out.read_text(encoding="utf-8"))
            npar = sum(len(s.get("paragraphs") or []) for s in data.get("sections") or [])
            print(f"  OK {npar} paragraphs, {len(data.get('sections') or [])} sections", flush=True)
            if npar < 3:
                failed.append((name, "too few paragraphs"))
            else:
                ok.append(name)
        except Exception as err:  # noqa: BLE001
            print(f"  FAIL {name}: {err}", flush=True)
            failed.append((name, str(err)))
    print("\nOK:", len(ok))
    print("FAIL:", len(failed))
    for name, err in failed:
        print(f" - {name}: {err}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
