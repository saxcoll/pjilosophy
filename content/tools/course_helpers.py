"""Shared constructors for course.json builders."""

PG = "Project Gutenberg"
MIT = "Internet Classics Archive (MIT)"
CCEL = "Christian Classics Ethereal Library"
WS = "Wikisource"


def src(name, url, locator, edition, license_="public-domain", available=True, note=None):
    d = {
        "name": name,
        "url": url,
        "locator": locator,
        "license": license_,
        "available": available,
        "edition": edition,
    }
    if note:
        d["note"] = note
    return d


def txt(tid, locator, scope="full", start=None, end=None):
    return {
        "id": tid,
        "path": f"texts/{tid}.json",
        "format": "json",
        "scope": scope,
        "start": start,
        "end": end,
        "locator": locator,
    }


def mc(n, prompt, a, b, c, d, correct, expl):
    return {
        "id": f"q{n}",
        "type": "multiple-choice",
        "prompt": prompt,
        "options": [
            {"id": "a", "text": a},
            {"id": "b", "text": b},
            {"id": "c", "text": c},
            {"id": "d", "text": d},
        ],
        "correct": correct,
        "explanation": expl,
    }


def tf(n, prompt, correct, expl):
    return {
        "id": f"q{n}",
        "type": "true-false",
        "prompt": prompt,
        "options": [
            {"id": "true", "text": "True"},
            {"id": "false", "text": "False"},
        ],
        "correct": correct,
        "explanation": expl,
    }


def ms(n, prompt, options, correct, expl):
    return {
        "id": f"q{n}",
        "type": "multiple-select",
        "prompt": prompt,
        "options": [{"id": oid, "text": text} for oid, text in options],
        "correct": correct,
        "explanation": expl,
    }


def make_quiz(assignment_id, title, intro, questions):
    return {
        "id": f"{assignment_id}-quiz",
        "title": title,
        "intro": intro,
        "questions": questions,
    }


def make_recap(unit_id, title, intro, questions):
    return {
        "id": f"{unit_id}-recap",
        "title": title,
        "intro": intro,
        "questions": questions,
    }


def A(
    id,
    order,
    kind,
    title,
    author,
    work,
    translator,
    selection,
    pages,
    minutes,
    why,
    look,
    questions,
    prereq,
    next_hint,
    source,
    text=None,
    quiz=None,
):
    d = {
        "id": id,
        "order": order,
        "kind": kind,
        "title": title,
        "author": author,
        "work": work,
        "translator": translator,
        "selection": selection,
        "pages": pages,
        "estimatedMinutes": minutes,
        "why": why,
        "lookFor": look,
        "questions": questions,
        "prerequisites": prereq,
        "nextHint": next_hint,
        "source": source,
    }
    if text:
        d["text"] = text
    if quiz:
        d["quiz"] = quiz
    return d
