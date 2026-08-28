#!/usr/bin/env python3
"""Re-split oversized/mis-sliced texts from content/_raw HTML and fetch remaining works."""
from __future__ import annotations

import json
import re
import ssl
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "content" / "_raw"
TEXTS = ROOT / "content" / "texts"
UA = "pjilosophy-course-ingest/1.0"
CTX = ssl.create_default_context()


class _HTMLText(HTMLParser):
    skip = {"script", "style", "noscript"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):  # noqa: ANN001
        if tag in self.skip:
            self._skip += 1
        if tag in {"p", "h1", "h2", "h3", "h4", "br", "div", "li"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):  # noqa: ANN001
        if tag in self.skip and self._skip:
            self._skip -= 1
        if tag in {"p", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_data(self, data):  # noqa: ANN001
        if not self._skip:
            self.parts.append(data)


def html_to_text(raw: str) -> str:
    p = _HTMLText()
    p.feed(raw)
    t = "".join(p.parts).replace("\r\n", "\n")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def paragraphs(text: str, min_len: int = 35) -> list[str]:
    out = []
    for chunk in re.split(r"\n\s*\n", text):
        line = re.sub(r"\s+", " ", chunk).strip()
        if len(line) >= min_len:
            out.append(line)
        elif 8 <= len(line) < min_len:
            out.append(line)
    return out


def fetch(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 800:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=CTX, timeout=90) as resp:
        dest.write_bytes(resp.read())
    return dest


def body_index(text: str, pattern: str) -> int | None:
    hits = [m.start() for m in re.finditer(pattern, text, re.I | re.M)]
    if not hits:
        return None
    cutoff = int(len(text) * 0.14)
    body = [h for h in hits if h >= cutoff]
    return (body or hits)[-1] if pattern.endswith(r"\b") and len(hits) > 3 else (body or hits)[0]


def split_by_patterns(text: str, specs: list[tuple[str, str, str, str]], cap: int = 140) -> list[dict]:
    """specs: (id, locator, heading, regex). Uses first body hit after TOC."""
    marks = []
    for sid, loc, head, pat in specs:
        idx = body_index(text, pat)
        if idx is not None:
            marks.append((idx, sid, loc, head))
    marks.sort()
    # unique increasing
    cleaned = []
    last = -1
    for m in marks:
        if m[0] > last:
            cleaned.append(m)
            last = m[0]
    sections = []
    for i, (start, sid, loc, head) in enumerate(cleaned):
        end = cleaned[i + 1][0] if i + 1 < len(cleaned) else len(text)
        paras = paragraphs(text[start:end])[:cap]
        if paras:
            sections.append({"id": sid, "locator": loc, "heading": head, "paragraphs": paras})
    return sections


def save(tid: str, title: str, author: str, translator: str, source: dict, attr: str, sections: list[dict]) -> None:
    payload = {
        "id": tid,
        "title": title,
        "author": author,
        "translator": translator,
        "language": "en",
        "license": "public-domain",
        "source": source,
        "attribution": attr,
        "sections": sections,
    }
    path = TEXTS / f"{tid}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n = sum(len(s["paragraphs"]) for s in sections)
    print(f"  wrote {tid}: {len(sections)} sections, {n} paras")


def main() -> None:
    # Burnet
    html = (RAW / "pg67097.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "burnet-early-greek",
        "Early Greek Philosophy (selections)",
        "John Burnet",
        "n/a (English original)",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/67097", "edition": "3rd ed.; PG #67097"},
        "John Burnet, Early Greek Philosophy. Public domain. Source: Project Gutenberg #67097.",
        split_by_patterns(
            text,
            [
                ("intro", "Introduction", "Introduction", r"\nINTRODUCTION\n"),
                ("milesians", "Chapter I. The Milesian School", "The Milesian School", r"CHAPTER I\s+THE MILESIAN SCHOOL"),
                ("science-religion", "Chapter II. Science and Religion", "Science and Religion", r"CHAPTER II\s+SCIENCE AND RELIGION"),
                ("heraclitus", "Chapter III. Herakleitos of Ephesos", "Herakleitos of Ephesos", r"CHAPTER III\s+HERAKLEITOS"),
                ("parmenides", "Chapter IV. Parmenides of Elea", "Parmenides of Elea", r"CHAPTER IV\s+PARMENIDES"),
                ("empedocles", "Chapter V. Empedokles of Akragas", "Empedokles of Akragas", r"CHAPTER V\s+EMPEDOKLES"),
                ("anaxagoras", "Chapter VI. Anaxagoras of Klazomenai", "Anaxagoras of Klazomenai", r"CHAPTER VI\s+ANAXAGORAS"),
                ("eleatics", "Chapter VIII. The Younger Eleatics", "The Younger Eleatics", r"CHAPTER VIII\s+THE YOUNGER ELEATICS"),
                ("atomists", "Chapter IX. Leukippos of Miletos", "Leukippos of Miletos", r"CHAPTER IX\s+LEUKIPPOS"),
            ],
            cap=160,
        ),
    )

    # Republic — keep I, II opening+IV, VI–VII
    html = (RAW / "pg55201.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "plato-republic",
        "Republic (Books I, II, IV, VI–VII)",
        "Plato",
        "Benjamin Jowett",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/55201", "edition": "Jowett 3rd ed. with Stephanus; PG #55201"},
        "Plato, Republic, trans. Benjamin Jowett. Public domain. Source: Project Gutenberg #55201.",
        split_by_patterns(
            text,
            [
                ("book-i", "Republic Book I (327–354)", "Book I", r"\nBOOK I\n"),
                ("book-ii", "Republic Book II (357–383)", "Book II", r"\nBOOK II\.?\n"),
                ("book-iv", "Republic Book IV (419–445)", "Book IV", r"\nBOOK IV\.?\n"),
                ("book-vi", "Republic Book VI (484–511)", "Book VI", r"\nBOOK VI\.?\n"),
                ("book-vii", "Republic Book VII (514–541)", "Book VII", r"\nBOOK VII\.?\n"),
            ],
            cap=180,
        ),
    )

    # Augustine VII, VIII, XI
    html = (RAW / "pg3296.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "augustine-confessions",
        "Confessions (Books VII, VIII, XI)",
        "Augustine of Hippo",
        "E. B. Pusey",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/3296", "edition": "Pusey; PG #3296"},
        "Augustine, Confessions, trans. E. B. Pusey. Public domain. Source: Project Gutenberg #3296.",
        split_by_patterns(
            text,
            [
                ("book-vii", "Book VII", "Book VII", r"\nBOOK VII\n"),
                ("book-viii", "Book VIII", "Book VIII", r"\nBOOK VIII\n"),
                ("book-xi", "Book XI", "Book XI", r"\nBOOK XI\n"),
            ],
            cap=120,
        ),
    )

    # Hume Dialogues II, X, XI
    html = (RAW / "pg4583.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "hume-dialogues",
        "Dialogues Concerning Natural Religion (Parts II, X–XI)",
        "David Hume",
        "n/a (English original)",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/4583", "edition": "PG #4583"},
        "David Hume, Dialogues Concerning Natural Religion. Public domain. Source: Project Gutenberg #4583.",
        split_by_patterns(
            text,
            [
                ("part-2", "Part II", "Part II", r"\nPART 2\n"),
                ("part-10", "Part X", "Part X", r"\nPART 10\n"),
                ("part-11", "Part XI", "Part XI", r"\nPART 11\n"),
            ],
            cap=90,
        ),
    )

    # Hume Enquiry sections via h2
    html = (RAW / "pg9662.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "hume-enquiry",
        "An Enquiry Concerning Human Understanding (selected sections)",
        "David Hume",
        "n/a (English original)",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/9662", "edition": "PG #9662"},
        "David Hume, An Enquiry Concerning Human Understanding. Public domain. Source: Project Gutenberg #9662.",
        split_by_patterns(
            text,
            [
                ("sec-2", "Section II. Of the Origin of Ideas", "Section II", r"SECTION II"),
                ("sec-4", "Section IV. Sceptical Doubts", "Section IV", r"SECTION IV"),
                ("sec-5", "Section V. Sceptical Solution", "Section V", r"SECTION V"),
                ("sec-7", "Section VII. Necessary Connexion", "Section VII", r"SECTION VII"),
                ("sec-8", "Section VIII. Liberty and Necessity", "Section VIII", r"SECTION VIII"),
                ("sec-10", "Section X. Of Miracles", "Section X", r"SECTION X"),
                ("sec-12", "Section XII. Academic Philosophy", "Section XII", r"SECTION XII"),
            ],
            cap=80,
        ),
    )

    # Descartes Meditations
    html = (RAW / "pg70091.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "descartes-meditations",
        "Meditations on First Philosophy",
        "René Descartes",
        "William Molyneux",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/70091", "edition": "Molyneux 1680; PG #70091"},
        "René Descartes, Six Metaphysical Meditations, trans. William Molyneux (1680). Public domain. Source: Project Gutenberg #70091.",
        split_by_patterns(
            text,
            [
                ("med-1", "Meditation I", "Meditation I. Of Things Doubtful", r"Meditat(?:ion|\.)\s*I\b|Of Things Doubtful"),
                ("med-2", "Meditation II", "Meditation II", r"Meditat(?:ion|\.)\s*II\b"),
                ("med-3", "Meditation III", "Meditation III", r"Meditat(?:ion|\.)\s*III\b"),
                ("med-4", "Meditation IV", "Meditation IV", r"Meditat(?:ion|\.)\s*IV\b"),
                ("med-5", "Meditation V", "Meditation V", r"Meditat(?:ion|\.)\s*V\b"),
                ("med-6", "Meditation VI", "Meditation VI", r"Meditat(?:ion|\.)\s*VI\b"),
            ],
            cap=70,
        ),
    )

    # Descartes Discourse
    html = (RAW / "pg59.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "descartes-discourse",
        "Discourse on the Method (Parts I–IV)",
        "René Descartes",
        "John Veitch",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/59", "edition": "Veitch; PG #59"},
        "René Descartes, Discourse on the Method, trans. John Veitch. Public domain. Source: Project Gutenberg #59.",
        split_by_patterns(
            text,
            [
                ("part-1", "Part I", "Part I", r"PART I\b"),
                ("part-2", "Part II", "Part II", r"PART II\b"),
                ("part-3", "Part III", "Part III", r"PART III\b"),
                ("part-4", "Part IV", "Part IV", r"PART IV\b"),
            ],
            cap=40,
        ),
    )

    # Marcus Books II–IV
    html = (RAW / "pg2680.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "marcus-meditations",
        "Meditations (Books II–IV)",
        "Marcus Aurelius",
        "George Long",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/2680", "edition": "Long; PG #2680"},
        "Marcus Aurelius, Meditations, trans. George Long. Public domain. Source: Project Gutenberg #2680.",
        split_by_patterns(
            text,
            [
                ("book-ii", "Book II", "Book II", r"THE SECOND BOOK|BOOK II\b"),
                ("book-iii", "Book III", "Book III", r"THE THIRD BOOK|BOOK III\b"),
                ("book-iv", "Book IV", "Book IV", r"THE FOURTH BOOK|BOOK IV\b"),
            ],
            cap=80,
        ),
    )

    # Locke Second Treatise chs
    html = (RAW / "pg7370.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "locke-second-treatise",
        "Second Treatise of Government (selected chapters)",
        "John Locke",
        "n/a (English original)",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/7370", "edition": "1690 text; PG #7370"},
        "John Locke, Second Treatise of Government. Public domain. Source: Project Gutenberg #7370.",
        split_by_patterns(
            text,
            [
                ("ch-2", "Chapter II. Of the State of Nature", "Chapter II", r"CHAPTER\.?\s*II\b"),
                ("ch-5", "Chapter V. Of Property", "Chapter V", r"CHAPTER\.?\s*V\b"),
                ("ch-8", "Chapter VIII. Of the Beginning of Political Societies", "Chapter VIII", r"CHAPTER\.?\s*VIII\b"),
                ("ch-19", "Chapter XIX. Of the Dissolution of Government", "Chapter XIX", r"CHAPTER\.?\s*XIX\b"),
            ],
            cap=70,
        ),
    )

    # Kant CPR
    html = (RAW / "pg4280.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "kant-cpr",
        "Critique of Pure Reason (Prefaces, Introduction, Aesthetic)",
        "Immanuel Kant",
        "J. M. D. Meiklejohn",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/4280", "edition": "Meiklejohn; PG #4280"},
        "Immanuel Kant, Critique of Pure Reason, trans. J. M. D. Meiklejohn. Public domain. Source: Project Gutenberg #4280.",
        split_by_patterns(
            text,
            [
                ("preface-a", "Preface to the first edition", "Preface A", r"PREFACE TO THE FIRST EDITION"),
                ("preface-b", "Preface to the second edition", "Preface B", r"PREFACE TO THE SECOND EDITION"),
                ("intro", "Introduction", "Introduction", r"\nINTRODUCTION\n"),
                ("aesthetic", "Transcendental Aesthetic", "Transcendental Aesthetic", r"TRANSCENDENTAL AESTHETIC"),
            ],
            cap=90,
        ),
    )

    # Mill Liberty
    html = (RAW / "pg34901.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "mill-on-liberty",
        "On Liberty (chs. I–III)",
        "John Stuart Mill",
        "n/a (English original)",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/34901", "edition": "PG #34901"},
        "John Stuart Mill, On Liberty. Public domain. Source: Project Gutenberg #34901.",
        split_by_patterns(
            text,
            [
                ("ch-1", "Chapter I", "Chapter I", r"CHAPTER I\b"),
                ("ch-2", "Chapter II", "Chapter II", r"CHAPTER II\b"),
                ("ch-3", "Chapter III", "Chapter III", r"CHAPTER III\b"),
            ],
            cap=70,
        ),
    )

    # Marx
    html = (RAW / "pg61.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "marx-manifesto",
        "The Communist Manifesto (I–II)",
        "Karl Marx and Friedrich Engels",
        "Samuel Moore",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/61", "edition": "Moore/Engels 1888; PG #61"},
        "Karl Marx and Friedrich Engels, The Communist Manifesto. Public domain. Source: Project Gutenberg #61.",
        split_by_patterns(
            text,
            [
                ("i", "I. Bourgeois and Proletarians", "I", r"I\.\s*BOURGEOIS AND PROLETARIANS"),
                ("ii", "II. Proletarians and Communists", "II", r"II\.\s*PROLETARIANS AND COMMUNISTS"),
            ],
            cap=80,
        ),
    )

    # Nietzsche Genealogy
    html = (RAW / "pg52319.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "nietzsche-genealogy",
        "The Genealogy of Morals (Preface, Essays I–II)",
        "Friedrich Nietzsche",
        "Horace B. Samuel",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/52319", "edition": "Samuel; PG #52319"},
        "Friedrich Nietzsche, The Genealogy of Morals, trans. Horace B. Samuel. Public domain. Source: Project Gutenberg #52319.",
        split_by_patterns(
            text,
            [
                ("preface", "Preface", "Preface", r"\nPREFACE\n"),
                ("essay-i", "First Essay", "First Essay", r"FIRST ESSAY"),
                ("essay-ii", "Second Essay", "Second Essay", r"SECOND ESSAY"),
            ],
            cap=90,
        ),
    )

    # Russell
    html = (RAW / "pg5827.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "russell-problems",
        "The Problems of Philosophy (chs. I, V, VI, XV)",
        "Bertrand Russell",
        "n/a (English original)",
        {"name": "Project Gutenberg", "url": "https://www.gutenberg.org/ebooks/5827", "edition": "1912; PG #5827"},
        "Bertrand Russell, The Problems of Philosophy (1912). Public domain. Source: Project Gutenberg #5827.",
        split_by_patterns(
            text,
            [
                ("ch-1", "Chapter I. Appearance and Reality", "Chapter I", r"CHAPTER I\.\s*APPEARANCE"),
                ("ch-5", "Chapter V", "Chapter V", r"CHAPTER V\."),
                ("ch-6", "Chapter VI. On Induction", "Chapter VI", r"CHAPTER VI\."),
                ("ch-15", "Chapter XV. The Value of Philosophy", "Chapter XV", r"CHAPTER XV\."),
            ],
            cap=50,
        ),
    )

    # Hegel lordship from already downloaded file (phba.htm is lordship)
    html = (RAW / "hegel-preface.html").read_text(encoding="utf-8", errors="replace")
    text = html_to_text(html)
    save(
        "hegel-phenomenology",
        "Phenomenology of Spirit: Lordship and Bondage",
        "G. W. F. Hegel",
        "J. B. Baillie",
        {
            "name": "Marxists Internet Archive (Baillie 1910)",
            "url": "https://www.marxists.org/reference/archive/hegel/works/ph/phba.htm",
            "edition": "Baillie 1910",
        },
        "G. W. F. Hegel, Phenomenology of Mind, trans. J. B. Baillie (1910). Public domain. Source: Marxists Internet Archive.",
        [{"id": "lordship", "locator": "B. Self-Consciousness: Lordship and Bondage", "heading": "Lordship and Bondage", "paragraphs": paragraphs(text)[:80]}],
    )

    # Remaining fetches
    try:
        dest = RAW / "epicurus-menoeceus.html"
        fetch("https://classics.mit.edu/Epicurus/menoec.html", dest)
        t = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
        save(
            "epicurus-menoeceus",
            "Letter to Menoeceus",
            "Epicurus",
            "Robert Drew Hicks",
            {"name": "Internet Classics Archive (MIT)", "url": "https://classics.mit.edu/Epicurus/menoec.html", "edition": "Hicks"},
            "Epicurus, Letter to Menoeceus, trans. Robert Drew Hicks. Public domain. Source: Internet Classics Archive.",
            [{"id": "full", "locator": "Complete letter", "heading": "Letter to Menoeceus", "paragraphs": paragraphs(t)}],
        )
    except Exception as err:
        print("FAIL epicurus", err)

    try:
        dest = RAW / "posterior-i.html"
        fetch("https://classics.mit.edu/Aristotle/posterior.1.i.html", dest)
        t = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
        save(
            "aristotle-posterior-analytics",
            "Posterior Analytics I",
            "Aristotle",
            "G. R. G. Mure",
            {"name": "Internet Classics Archive (MIT)", "url": "https://classics.mit.edu/Aristotle/posterior.1.i.html", "edition": "Mure"},
            "Aristotle, Posterior Analytics, trans. G. R. G. Mure. Public domain. Source: Internet Classics Archive.",
            [{"id": "pa-i", "locator": "Posterior Analytics Book I (opening)", "heading": "Book I", "paragraphs": paragraphs(t)[:70]}],
        )
    except Exception as err:
        print("FAIL posterior", err)

    try:
        dest = RAW / "tractatus.html"
        fetch("https://en.wikisource.org/wiki/Tractatus_Logico-Philosophicus", dest)
        t = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
        paras = paragraphs(t)
        save(
            "wittgenstein-tractatus",
            "Tractatus Logico-Philosophicus (Ogden)",
            "Ludwig Wittgenstein",
            "C. K. Ogden",
            {"name": "Wikisource", "url": "https://en.wikisource.org/wiki/Tractatus_Logico-Philosophicus", "edition": "Ogden 1922"},
            "Ludwig Wittgenstein, Tractatus Logico-Philosophicus, trans. C. K. Ogden (1922). Public domain. Source: Wikisource.",
            [
                {"id": "p1", "locator": "Propositions 1–3", "heading": "World and picture", "paragraphs": paras[:80]},
                {"id": "p4", "locator": "Propositions 4–5", "heading": "Thought and proposition", "paragraphs": paras[80:160]},
                {"id": "p6", "locator": "Propositions 6–7", "heading": "The general form; silence", "paragraphs": paras[160:240]},
            ]
            if len(paras) > 50
            else [{"id": "full", "locator": "Tractatus", "heading": "Tractatus", "paragraphs": paras}],
        )
    except Exception as err:
        print("FAIL tractatus", err)

    try:
        dest = RAW / "plotinus-v1.html"
        fetch("https://en.wikisource.org/wiki/Plotinus_(MacKenna)/The_Divine_Mind", dest)
        t = html_to_text(dest.read_text(encoding="utf-8", errors="replace"))
        save(
            "plotinus-enneads",
            "The Enneads (Fifth Ennead, MacKenna)",
            "Plotinus",
            "Stephen MacKenna",
            {"name": "Wikisource", "url": "https://en.wikisource.org/wiki/Plotinus_(MacKenna)", "edition": "MacKenna"},
            "Plotinus, The Enneads, trans. Stephen MacKenna. Public domain. Source: Wikisource.",
            [{"id": "v-1", "locator": "Fifth Ennead (The Divine Mind)", "heading": "The Divine Mind", "paragraphs": paragraphs(t)[:90]}],
        )
    except Exception as err:
        print("FAIL plotinus", err)

    # Trim a few remaining giants in place if still huge
    for name, cap in [
        ("maimonides-guide", 80),
        ("hume-treatise", 60),
        ("spinoza-ethics", 100),
        ("james-will-to-believe", 70),
        ("moore-principia-ethica", 80),
        ("nietzsche-gay-science", 80),
        ("bacon-novum-organum", 90),
        ("smith-tms", 70),
        ("hobbes-leviathan", 80),
        ("boethius-consolation", 80),
        ("anselm-proslogion", 70),
    ]:
        path = TEXTS / f"{name}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for sec in data.get("sections") or []:
            if len(sec.get("paragraphs") or []) > cap:
                sec["paragraphs"] = sec["paragraphs"][:cap]
                changed = True
        if changed:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  trimmed {name}")


if __name__ == "__main__":
    main()
