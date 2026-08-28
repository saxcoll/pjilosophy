#!/usr/bin/env python3
"""Download Wikimedia Commons portraits into content/images/thinkers/ and write thinkers.json."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
CONTENT = TOOLS.parent
IMG_DIR = CONTENT / "images" / "thinkers"
UA = "pjilosophy-course/1.0 (educational static site; https://github.com/)"

# thinker id, display name, sort name, candidate Commons filenames (first that is freely licensed wins)
CATALOG = [
    ("thales", "Thales", "Thales", ["Illustrerad Verldshistoria band I Ill 107.jpg", "Thales.jpg"]),
    ("anaximander", "Anaximander", "Anaximander", ["Anaximander Mosaic.jpg", "Anaximander.jpg"]),
    ("anaximenes", "Anaximenes", "Anaximenes", ["Anaximenes.jpg"]),
    ("xenophanes", "Xenophanes", "Xenophanes", ["Xenophanes in Thomas Stanley History of Philosophy.jpg"]),
    ("heraclitus", "Heraclitus", "Heraclitus", [
        "Johannes Moreelse - Heraclitus - Google Art Project.jpg",
        "Hendrik ter Brugghen - Heraclitus.jpg",
        "Heraclitus, Johannes Moreelse.jpg",
    ]),
    ("parmenides", "Parmenides", "Parmenides", ["Parmenides.jpg", "Bust Parmenides Velia.jpg"]),
    ("zeno", "Zeno of Elea", "Zeno", [
        "Zeno of Elea Tibaldi or Carducci Escorial.jpg",
        "Portret van Zeno van Elea Zenon Philosophe. (titel op object), RP-P-1908-401.jpg",
    ]),
    ("empedocles", "Empedocles", "Empedocles", ["Empedocles in Thomas Stanley History of Philosophy.jpg"]),
    ("anaxagoras", "Anaxagoras", "Anaxagoras", ["Anaxagoras Lebiedzki Rahl.jpg", "Anaxagoras Nuremberg Chronicle.jpg"]),
    ("democritus", "Democritus", "Democritus", ["Hendrik ter Brugghen - Democritus.jpg", "Democritus2.jpg"]),
    ("leucippus", "Leucippus", "Leucippus", []),
    ("socrates", "Socrates", "Socrates", ["Socrates Louvre.jpg", "Portrait of Socrates Marble, Roman artwork.jpg"]),
    ("plato", "Plato", "Plato", ["Plato Silanion Musei Capitolini MC1377.jpg", "Plato-raphael.jpg"]),
    ("aristotle", "Aristotle", "Aristotle", ["Aristotle Altemps Inv8575.jpg", "Aristotle_by_Raphael.jpg"]),
    ("epicurus", "Epicurus", "Epicurus", ["Epicurus Louvre.jpg", "Epicurus bust2.jpg"]),
    ("lucretius", "Lucretius", "Lucretius", ["Lucretius1.png", "Titus Lucretius Carus.jpg"]),
    ("epictetus", "Epictetus", "Epictetus", ["Epictetus.jpg", "Artgate Fondazione Cariplo - Cunego Domenico, Epitteto.jpg"]),
    ("marcus-aurelius", "Marcus Aurelius", "Marcus Aurelius", [
        "Marble bust of Marcus Aurelius - Palazzo Nuovo - Musei Capitolini - Rome 2016.jpg",
        "Marcus Aurelius Glyptothek Munich.jpg",
    ]),
    ("sextus-empiricus", "Sextus Empiricus", "Sextus Empiricus", [
        "Sextus Empiricus - engraving by G. F. Riedel - 1801.jpg",
        "Sextus.jpg",
    ]),
    ("plotinus", "Plotinus", "Plotinus", ["Plotinus.jpg", "Head of a philosopher - possible Plotinus.jpg"]),
    ("boethius", "Boethius", "Boethius", ["Boethius.jpg", "Boethius consolation philosophy manuscript.jpg"]),
    ("augustine", "Augustine of Hippo", "Augustine", ["Saint Augustine by Philippe de Champaigne.jpg", "Botticelli, Sandro - Saint Augustine.jpg"]),
    ("anselm", "Anselm of Canterbury", "Anselm", ["Anselm of Canterbury.jpg", "Anselm-Canterbury.jpg"]),
    ("averroes", "Averroes", "Averroes", [
        "Ibn rushd.jpg",
        "Statue of Averroes in Córdoba, Spain.jpg",
        "AverroesCloseup.jpg",
    ]),
    ("maimonides", "Maimonides", "Maimonides", ["Maimonides-2.jpg", "Maimonides portrait.jpg"]),
    ("aquinas", "Thomas Aquinas", "Aquinas", ["St-thomas-aquinas.jpg", "Thomas Aquinas by Fra Angelico.jpg"]),
    ("bacon", "Francis Bacon", "Bacon", ["Somer Francis Bacon.jpg", "Francis Bacon, Viscount St Alban from NPG.jpg"]),
    ("descartes", "René Descartes", "Descartes", ["Frans Hals - Portret van René Descartes.jpg", "Andre Thevet-Rene Descartes.jpg"]),
    ("spinoza", "Baruch Spinoza", "Spinoza", ["Spinoza.jpg", "Baruch de Spinoza.jpg"]),
    ("pascal", "Blaise Pascal", "Pascal", ["Blaise Pascal 2.jpg", "Blaise Pascal Versailles.jpg"]),
    ("leibniz", "Gottfried Wilhelm Leibniz", "Leibniz", ["Gottfried Wilhelm Leibniz, Bernhard Christoph Francke.jpg", "Christoph Bernhard Francke - Bildnis des Philosophen Leibniz.jpg"]),
    ("hobbes", "Thomas Hobbes", "Hobbes", ["Thomas Hobbes (portrait).jpg", "Thomas Hobbes by John Michael Wright.jpg"]),
    ("locke", "John Locke", "Locke", ["JohnLocke.png", "Godfrey Kneller - Portrait of John Locke.jpg"]),
    ("berkeley", "George Berkeley", "Berkeley", ["John Smibert - Bishop George Berkeley.jpg", "George Berkeley by John Smibert.jpg"]),
    ("hume", "David Hume", "Hume", [
        "Allan Ramsay - David Hume, 1711 - 1776. Historian and philosopher - Google Art Project.jpg",
        "David Hume.jpg",
    ]),
    ("rousseau", "Jean-Jacques Rousseau", "Rousseau", ["Jean-Jacques Rousseau (painted portrait).jpg", "Maurice Quentin de La Tour - Portrait of Jean-Jacques Rousseau.jpg"]),
    ("adam-smith", "Adam Smith", "Smith", ["AdamSmith.jpg", "Adam Smith The Muir portrait.jpg"]),
    ("kant", "Immanuel Kant", "Kant", ["Kant gemaelde 3.jpg", "Immanuel Kant (painted portrait).jpg"]),
    ("hegel", "G. W. F. Hegel", "Hegel", ["Hegel portrait by Schlesinger 1831.jpg", "Georg Wilhelm Friedrich Hegel by Schlesinger.jpg"]),
    ("schopenhauer", "Arthur Schopenhauer", "Schopenhauer", ["Schopenhauer.jpg", "Arthur Schopenhauer by J Schafer, 1859.jpg"]),
    ("mill", "John Stuart Mill", "Mill", ["John Stuart Mill by London Stereoscopic Company, c1870.jpg", "John Stuart Mill by George Frederic Watts.jpg"]),
    ("kierkegaard", "Søren Kierkegaard", "Kierkegaard", ["Kierkegaard.jpg", "Soren Kierkegaard.jpg"]),
    ("marx", "Karl Marx", "Marx", ["Karl Marx 001.jpg", "Karl Marx.jpg"]),
    ("engels", "Friedrich Engels", "Engels", ["Friedrich Engels portrait.jpg", "Friedrich Engels.jpg"]),
    ("nietzsche", "Friedrich Nietzsche", "Nietzsche", ["Nietzsche187a.jpg", "Friedrich Nietzsche 1882.jpg"]),
    ("peirce", "Charles Sanders Peirce", "Peirce", ["Charles Sanders Peirce.jpg", "Charles Sanders Peirce portrait.jpg"]),
    ("james", "William James", "James", ["William James b1842c.jpg", "William James.jpg"]),
    ("dewey", "John Dewey", "Dewey", ["John Dewey cph.3a51565.jpg", "John Dewey in 1902.jpg"]),
    ("du-bois", "W. E. B. Du Bois", "Du Bois", ["WEB DuBois 1918.jpg", "W.E.B. Du Bois by James E. Purdy, 1907.jpg"]),
    ("moore", "G. E. Moore", "Moore", [
        "G. E. Moore c. 1903.jpg",
        "1914 George Edward Moore (cropped).jpg",
        "G. E. Moore young.jpg",
    ]),
    ("russell", "Bertrand Russell", "Russell", ["Bertrand Russell 1916.jpg", "Russell1916.jpg", "Bertrand Russell photo.jpg"]),
    ("wittgenstein", "Ludwig Wittgenstein", "Wittgenstein", ["Ludwig Wittgenstein.jpg", "Ludwig Wittgenstein 1929.jpg", "Wittgenstein.jpg"]),
    ("burnet", "John Burnet", "Burnet", ["John Burnet philosopher.jpg"]),
    ("gaunilo", "Gaunilo of Marmoutiers", "Gaunilo", []),
    ("heidegger", "Martin Heidegger", "Heidegger", []),
    ("sartre", "Jean-Paul Sartre", "Sartre", []),
    ("quine", "W. V. O. Quine", "Quine", []),
    ("anscombe", "G. E. M. Anscombe", "Anscombe", []),
    ("rawls", "John Rawls", "Rawls", []),
    ("foucault", "Michel Foucault", "Foucault", []),
    ("murdoch", "Iris Murdoch", "Murdoch", []),
]

FREE_RX = re.compile(
    r"(public domain|pd-|cc0|cc-zero|cc by|cc-by|creative commons attribution)",
    re.I,
)
BLOCK_RX = re.compile(r"(fair use|noncommercial|cc by-nc|all rights reserved|copyrighted)", re.I)


def api_get(params: dict) -> dict:
    params = dict(params)
    params["format"] = "json"
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def license_ok(meta: dict) -> tuple[bool, str]:
    def val(key):
        block = meta.get(key) or {}
        return (block.get("value") or "").strip()

    short = val("LicenseShortName") or val("License")
    usage = val("UsageTerms")
    blob = f"{short} {usage}"
    if BLOCK_RX.search(blob) and not FREE_RX.search(blob):
        return False, short or usage
    if FREE_RX.search(blob):
        license_id = "public-domain"
        low = blob.lower()
        if "cc by-sa" in low or "cc-by-sa" in low or "sharealike" in low:
            license_id = "cc-by-sa"
        elif re.search(r"cc by\b|cc-by\b|attribution", low) and "sa" not in low.split("by")[-1][:8]:
            if "sharealike" in low:
                license_id = "cc-by-sa"
            elif "public domain" in low or "cc0" in low:
                license_id = "public-domain"
            else:
                license_id = "cc-by" if "cc" in low else "public-domain"
        return True, license_id
    return False, short or usage or "unknown"


def file_info(title: str) -> dict | None:
    if not title.lower().startswith("file:"):
        title = "File:" + title
    data = api_get(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size|mime|canonicaltitle",
            "iiurlwidth": "700",
        }
    )
    pages = (data.get("query") or {}).get("pages") or {}
    page = next(iter(pages.values()), None)
    if not page or page.get("missing") is not None:
        return None
    infos = page.get("imageinfo") or []
    if not infos:
        return None
    return infos[0]


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        dest.write_bytes(resp.read())


def shrink(path: Path) -> None:
    jpg = path.with_suffix(".jpg")
    cmd = [
        "sips",
        "-Z",
        "900",
        "-s",
        "format",
        "jpeg",
        "-s",
        "formatOptions",
        "72",
        str(path),
        "--out",
        str(jpg),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if path != jpg and path.exists():
        path.unlink()
    # recompress if still huge
    if jpg.exists() and jpg.stat().st_size > 220_000:
        subprocess.run(
            ["sips", "-Z", "700", "-s", "formatOptions", "60", str(jpg), "--out", str(jpg)],
            check=True,
            capture_output=True,
        )


def main() -> int:
    from course_thinkers import NAMES

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    # include every named thinker, even if not in CATALOG
    catalog_ids = {row[0] for row in CATALOG}
    extra = [i for i in NAMES if i not in catalog_ids]
    rows = list(CATALOG) + [(i, NAMES[i], NAMES[i], []) for i in extra]

    thinkers = []
    with_img = 0
    without = 0
    prev = {}
    prev_path = CONTENT / "thinkers.json"
    if prev_path.exists():
        prev = {t["id"]: t for t in json.loads(prev_path.read_text()).get("thinkers") or []}
    for tid, name, sort, files in rows:
        record = {"id": tid, "name": name, "sortName": sort}
        existing = IMG_DIR / f"{tid}.jpg"
        if existing.exists() and existing.stat().st_size > 1000:
            old = prev.get(tid) or {}
            record["image"] = f"images/thinkers/{tid}.jpg"
            if old.get("imageCredit"):
                record["imageCredit"] = old["imageCredit"]
            if old.get("license"):
                record["license"] = old["license"]
            with_img += 1
            print(f"KEEP {tid}")
            thinkers.append(record)
            continue
        chosen = None
        credit = None
        lic = None
        for fname in files:
            try:
                info = file_info(fname)
            except Exception as e:
                print(f"  skip {tid} {fname}: {e}", file=sys.stderr)
                continue
            if not info:
                print(f"  missing file {fname}")
                continue
            meta = info.get("extmetadata") or {}
            ok, lic_id = license_ok(meta)
            if not ok:
                print(f"  skip license {fname}: {lic_id}")
                continue
            thumb = info.get("thumburl") or info.get("url")
            if not thumb:
                continue
            artist = ((meta.get("Artist") or {}).get("value") or "Unknown").strip()
            artist = re.sub(r"<[^>]+>", "", artist)
            artist = artist.replace("Unknown authorUnknown author", "Unknown")
            desc = ((meta.get("ObjectName") or meta.get("ImageDescription") or {}).get("value") or fname).strip()
            desc = re.sub(r"<[^>]+>", "", desc)
            desc = re.sub(r"\s+", " ", desc)[:180]
            page_url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(
                info.get("canonicaltitle") or ("File:" + fname)
            )
            chosen = thumb
            lic = lic_id
            credit = f"Wikimedia Commons — {desc}. {artist}. {lic_id}. {page_url}"
            break
        if chosen:
            raw = IMG_DIR / f"{tid}.download"
            try:
                download(chosen, raw)
                shrink(raw)
                out = IMG_DIR / f"{tid}.jpg"
                if out.exists() and out.stat().st_size > 1000:
                    record["image"] = f"images/thinkers/{tid}.jpg"
                    record["imageCredit"] = credit
                    record["license"] = lic
                    with_img += 1
                    print(f"OK {tid} ({out.stat().st_size} bytes)")
                else:
                    without += 1
                    print(f"FAIL empty {tid}")
            except Exception as e:
                without += 1
                print(f"FAIL {tid}: {e}", file=sys.stderr)
                if raw.exists():
                    raw.unlink()
        else:
            without += 1
            print(f"NO IMAGE {tid}")
        thinkers.append(record)

    out = CONTENT / "thinkers.json"
    out.write_text(json.dumps({"thinkers": thinkers}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    print(f"with images: {with_img}; without: {without}; total: {len(thinkers)}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(TOOLS))
    raise SystemExit(main())
