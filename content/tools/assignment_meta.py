"""Difficulty (1–3) and word counts for assignments.

Word counts are computed from hosted `content/texts/*.json` for the
assigned `text.start`/`text.end` range. Bibliographic sittings omit
wordCount rather than inventing a number.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent

# 1 accessible (Apology, Crito, short Mill) · 2 intermediate (Hume Enquiry,
# Descartes Meditations, NE I) · 3 advanced (Spinoza Ethics, Kant CPR,
# Metaphysics, Hegel, Tractatus).
DIFFICULTY: dict[str, int] = {
    "burnet-introduction": 1,
    "milesian-school": 1,
    "xenophanes-poets": 1,
    "heraclitus-fragments": 2,
    "parmenides-truth": 3,
    "zeno-paradoxes": 2,
    "empedocles-anaxagoras": 2,
    "atomists-leucippus": 2,
    "plato-euthyphro": 1,
    "plato-apology": 1,
    "plato-crito": 1,
    "plato-meno-inquiry": 2,
    "plato-meno-knowledge": 2,
    "plato-republic-book-i": 2,
    "plato-republic-soul-city": 2,
    "plato-republic-cave": 2,
    "aristotle-categories-substance": 2,
    "aristotle-physics-nature": 2,
    "aristotle-ne-happiness": 2,
    "aristotle-ne-virtue": 2,
    "aristotle-metaphysics-wisdom": 3,
    "aristotle-posterior-analytics": 3,
    "epicurus-menoeceus": 1,
    "lucretius-atoms": 2,
    "lucretius-death": 1,
    "epictetus-enchiridion-i": 1,
    "epictetus-enchiridion-ii": 1,
    "marcus-meditations": 1,
    "sextus-outlines-i": 2,
    "plotinus-hypostases": 3,
    "boethius-consolation": 2,
    "augustine-confessions-evil": 2,
    "augustine-confessions-will": 2,
    "augustine-confessions-time": 2,
    "anselm-proslogion": 2,
    "gaunilo-and-reply": 2,
    "averroes-decisive": 2,
    "maimonides-guide": 2,
    "aquinas-sacred-doctrine": 2,
    "aquinas-five-ways": 2,
    "aquinas-natural-law": 2,
    "bacon-idols": 1,
    "descartes-discourse": 1,
    "descartes-meditations-1-2": 2,
    "descartes-meditations-3-4": 2,
    "descartes-meditations-5-6": 2,
    "spinoza-ethics-god": 3,
    "pascal-pensees": 2,
    "leibniz-monadology": 3,
    "hobbes-state-of-nature": 1,
    "hobbes-sovereign": 2,
    "locke-property": 2,
    "locke-no-innate": 2,
    "locke-qualities": 2,
    "berkeley-principles": 2,
    "hume-enquiry-ideas": 2,
    "hume-enquiry-causation": 2,
    "hume-enquiry-miracles": 2,
    "hume-treatise-identity": 3,
    "hume-dialogues-design": 2,
    "rousseau-inequality": 2,
    "rousseau-contract-i": 2,
    "rousseau-contract-ii": 2,
    "smith-moral-sentiments": 2,
    "kant-cpr-prefaces": 3,
    "kant-groundwork-i": 2,
    "kant-groundwork-ii": 3,
    "hegel-lordship": 3,
    "schopenhauer-will": 2,
    "mill-utilitarianism": 1,
    "mill-liberty-harm": 1,
    "mill-liberty-individuality": 1,
    "kierkegaard-fear": 2,
    "marx-manifesto": 1,
    "nietzsche-genealogy-i": 2,
    "nietzsche-genealogy-ii": 2,
    "nietzsche-gay-science": 2,
    "peirce-ideas-clear": 2,
    "james-pragmatism": 1,
    "james-will-to-believe": 1,
    "dewey-reconstruction": 2,
    "dubois-souls": 1,
    "moore-principia": 2,
    "russell-problems-appearance": 1,
    "russell-problems-induction": 2,
    "tractatus-picture": 3,
    "tractatus-silence": 3,
    "wittgenstein-investigations": 2,
    "husserl-psychologism": 3,
    "husserl-intentionality": 3,
    "husserl-ideas-reduction": 3,
    "husserl-transcendental": 3,
    "heidegger-being-time": 3,
    "sartre-existentialism": 1,
    "popper-lsd": 3,
    "quine-two-dogmas": 3,
    "kuhn-ssr": 2,
    "anscombe-modern-moral": 2,
    "rawls-justice": 2,
    "foucault-discipline": 2,
    "murdoch-sovereignty": 2,
    "map-analytic": 2,
    "map-continental-ethics": 2,
}

_WORD_RE = re.compile(r"\S+")
_text_cache: dict[str, dict] = {}


def _load_text(tid: str) -> dict | None:
    if tid in _text_cache:
        return _text_cache[tid]
    path = CONTENT / "texts" / f"{tid}.json"
    if not path.exists():
        _text_cache[tid] = None  # type: ignore[assignment]
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    _text_cache[tid] = data
    return data


def _section_words(section: dict) -> int:
    n = 0
    for p in section.get("paragraphs") or []:
        if isinstance(p, str):
            n += len(_WORD_RE.findall(p))
    return n


def count_assigned_words(pointer: dict) -> int | None:
    """Words in the hosted sections this assignment actually points at."""
    tid = pointer.get("id")
    if not tid:
        return None
    data = _load_text(tid)
    if not data:
        return None
    sections = data.get("sections") or []
    if not sections:
        return None
    start = pointer.get("start")
    end = pointer.get("end")
    ids = [s.get("id") for s in sections]
    if not start:
        chosen = sections
    else:
        try:
            i0 = ids.index(start)
        except ValueError:
            return None
        if not end or end == start:
            chosen = [sections[i0]]
        else:
            try:
                i1 = ids.index(end)
            except ValueError:
                return None
            if i0 <= i1:
                chosen = sections[i0 : i1 + 1]
            else:
                # Sections stored out of pedagogical order: count the two named ends.
                chosen = [sections[i0], sections[i1]]
    total = sum(_section_words(s) for s in chosen)
    return total if total > 0 else None


def apply_assignment_meta(course: dict) -> list[str]:
    errors = []
    missing_diff = []
    for era in course.get("eras") or []:
        for unit in era.get("units") or []:
            for a in unit.get("assignments") or []:
                aid = a.get("id")
                diff = DIFFICULTY.get(aid)
                if diff not in (1, 2, 3):
                    missing_diff.append(aid or "?")
                    continue
                a["difficulty"] = diff
                pointer = a.get("text")
                if isinstance(pointer, dict):
                    n = count_assigned_words(pointer)
                    if n is not None:
                        a["wordCount"] = n
                    else:
                        a.pop("wordCount", None)
                else:
                    a.pop("wordCount", None)
    if missing_diff:
        errors.append("assignments missing difficulty: " + ", ".join(missing_diff))
    extra = sorted(set(DIFFICULTY) - {
        a["id"]
        for era in course.get("eras") or []
        for unit in era.get("units") or []
        for a in unit.get("assignments") or []
    })
    if extra:
        errors.append("difficulty map has unused ids: " + ", ".join(extra))
    return errors
