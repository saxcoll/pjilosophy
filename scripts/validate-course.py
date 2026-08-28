#!/usr/bin/env python3
"""Defensive check: the UI must not assume optional course fields exist."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = [ROOT / "content" / "course.json", ROOT / "course.json"]


def fail_list() -> list[str]:
    return []


def main() -> int:
    path = next((p for p in CANDIDATES if p.exists()), None)
    if not path:
        print("No course.json found.", file=sys.stderr)
        return 1

    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if not isinstance(data.get("course"), dict):
        errors.append("missing course object")
    if not isinstance(data.get("eras"), list):
        errors.append("eras must be an array")

    ids: set[str] = set()
    assignment_count = 0
    quiz_count = 0
    recap_count = 0
    optional = {
        "translator": 0,
        "locator": 0,
        "themes": 0,
        "prerequisites": 0,
        "lookFor": 0,
        "questions": 0,
    }

    for era in data.get("eras") or []:
        if not era or not era.get("id"):
            errors.append("era missing id")
        if str(era.get("id") or "").startswith("stub-"):
            errors.append(f"stub era still present: {era.get('id')}")
        if era.get("themes") in (None, []):
            optional["themes"] += 1
        units = era.get("units") or []
        if not isinstance(units, list):
            errors.append(f"era {era.get('id')} units is not an array")
            continue
        for unit in units:
            if not unit or not unit.get("id"):
                errors.append("unit missing id")
            recap = unit.get("recapQuiz") if unit else None
            if isinstance(recap, dict) and recap.get("questions"):
                recap_count += 1
            for a in unit.get("assignments") or []:
                assignment_count += 1
                aid = a.get("id") if a else None
                if not aid:
                    errors.append("assignment missing id")
                elif aid in ids:
                    errors.append(f"duplicate assignment id {aid}")
                else:
                    ids.add(aid)
                if a and not a.get("title") and not a.get("work"):
                    errors.append(f"assignment {aid} needs title or work")
                kind = a.get("kind") if a else None
                if kind not in ("primary", "secondary", "bibliographic", None):
                    errors.append(f"assignment {aid} has unexpected kind {kind}")
                if a and not a.get("translator"):
                    optional["translator"] += 1
                source = (a or {}).get("source") or {}
                if source.get("locator") in (None, ""):
                    optional["locator"] += 1
                if not a.get("prerequisites"):
                    optional["prerequisites"] += 1
                if not a.get("lookFor"):
                    optional["lookFor"] += 1
                if not a.get("questions"):
                    optional["questions"] += 1
                quiz = a.get("quiz") if a else None
                if isinstance(quiz, dict) and quiz.get("questions"):
                    quiz_count += 1
                if str(aid or "").startswith("stub-"):
                    errors.append(f"stub assignment still present: {aid}")

    # Sparse assignment: missing optional fields must still flatten.
    sparse = {
        "course": {"id": "t", "title": "T"},
        "eras": [
            {
                "id": "e",
                "order": 1,
                "title": "E",
                "units": [
                    {
                        "id": "u",
                        "order": 1,
                        "title": "U",
                        "assignments": [
                            {
                                "id": "sparse-1",
                                "order": 1,
                                "kind": "primary",
                                "title": "Bare",
                                "author": "Anon",
                                "work": "Fragments",
                                "source": {"available": True, "url": "https://example.org"},
                            }
                        ],
                    }
                ],
            }
        ],
    }
    flat = []
    for era in sorted(sparse["eras"], key=lambda x: x.get("order") or 0):
        for unit in sorted(era.get("units") or [], key=lambda x: x.get("order") or 0):
            for assignment in sorted(unit.get("assignments") or [], key=lambda x: x.get("order") or 0):
                _ = assignment.get("translator") or ""
                _ = (assignment.get("source") or {}).get("locator") or ""
                _ = era.get("themes") or []
                _ = assignment.get("prerequisites") or []
                flat.append(assignment["id"])
    if flat != ["sparse-1"]:
        errors.append("sparse flatten failed")

    if errors:
        print(f"FAIL {path}", file=sys.stderr)
        for e in errors:
            print(" -", e, file=sys.stderr)
        return 1

    print(f"OK {path}")
    print(f"  eras: {len(data.get('eras') or [])}")
    print(f"  assignments: {assignment_count}")
    print(f"  assignment quizzes: {quiz_count}")
    print(f"  unit recap quizzes: {recap_count}")
    print(f"  optional-field gaps (must be safe): {optional}")
    print("  sparse missing-field flatten: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
