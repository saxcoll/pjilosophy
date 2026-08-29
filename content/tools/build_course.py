#!/usr/bin/env python3
"""Assemble content/course.json (and the repo-root fallback copy)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent.parent
CONTENT = ROOT / "content"
sys.path.insert(0, str(TOOLS))

from course_eras1 import course_meta, era_presocratic  # noqa: E402
from course_eras2 import era_classical  # noqa: E402
from course_eras3 import (  # noqa: E402
    era_early_modern,
    era_hellenistic,
    era_late_antiquity,
    era_medieval,
)
from course_eras4 import era_empiricism, era_enlightenment  # noqa: E402
from course_eras5 import era_nineteenth, era_present, era_twentieth_pd  # noqa: E402
from course_thinkers import apply_thinkers  # noqa: E402
from assignment_meta import apply_assignment_meta  # noqa: E402
from quizzes import all_quizzes, recap_quizzes  # noqa: E402


def attach(course: dict) -> dict:
    quizzes = all_quizzes()
    recaps = recap_quizzes()
    missing_quiz = []
    extra_quiz = set(quizzes)
    recap_applied = []
    recap_skipped_small = []

    for era in course["eras"]:
        for unit in era["units"]:
            assignments = unit.get("assignments") or []
            for a in assignments:
                aid = a["id"]
                extra_quiz.discard(aid)
                quiz = quizzes.get(aid)
                if quiz:
                    a["quiz"] = quiz
                else:
                    missing_quiz.append(aid)
            if len(assignments) >= 3:
                uid = unit["id"]
                recap = recaps.get(uid)
                if recap:
                    unit["recapQuiz"] = recap
                    recap_applied.append(uid)
                else:
                    recap_skipped_small.append(uid)
            elif recaps.get(unit["id"]):
                recap_skipped_small.append(f"{unit['id']} (has recap but <3 assignments)")

    unused_recaps = [uid for uid in recaps if uid not in recap_applied]
    return {
        "missing_quiz": missing_quiz,
        "extra_quiz": sorted(extra_quiz),
        "recap_applied": recap_applied,
        "recap_missing_for_large_units": [
            uid
            for era in course["eras"]
            for unit in era["units"]
            if len(unit.get("assignments") or []) >= 3 and "recapQuiz" not in unit
        ],
        "unused_recaps": unused_recaps,
    }


def validate_quizzes(course: dict) -> list[str]:
    errors: list[str] = []
    quiz_ids: set[str] = set()
    recap_ids: set[str] = set()

    def check_questions(owner: str, quiz: dict, min_q: int, max_q: int) -> None:
        qid = quiz.get("id")
        if not qid:
            errors.append(f"{owner}: quiz missing id")
            return
        questions = quiz.get("questions") or []
        if not min_q <= len(questions) <= max_q:
            errors.append(f"{qid}: expected {min_q}–{max_q} questions, got {len(questions)}")
        seen = set()
        for i, q in enumerate(questions, 1):
            if q.get("id") in seen:
                errors.append(f"{qid}: duplicate question id {q.get('id')}")
            seen.add(q.get("id"))
            qtype = q.get("type")
            if qtype not in ("multiple-choice", "true-false", "multiple-select"):
                errors.append(f"{qid} {q.get('id')}: bad type {qtype}")
            options = q.get("options") or []
            opt_ids = [o.get("id") for o in options]
            correct = q.get("correct")
            if qtype == "multiple-select":
                if not isinstance(correct, list) or len(correct) < 2:
                    errors.append(f"{qid} {q.get('id')}: multiple-select needs 2+ correct ids")
                elif any(c not in opt_ids for c in correct):
                    errors.append(f"{qid} {q.get('id')}: correct id not in options")
                if len(options) < 4:
                    errors.append(f"{qid} {q.get('id')}: multiple-select needs 4+ options")
            else:
                if correct not in opt_ids:
                    errors.append(f"{qid} {q.get('id')}: correct {correct!r} not in options")
            if qtype == "true-false" and opt_ids != ["true", "false"]:
                errors.append(f"{qid} {q.get('id')}: true-false options must be true/false")
            if qtype == "multiple-choice" and len(options) != 4:
                errors.append(f"{qid} {q.get('id')}: multiple-choice needs 4 options")
            if not q.get("prompt") or not q.get("explanation"):
                errors.append(f"{qid} {q.get('id')}: missing prompt or explanation")

    for era in course["eras"]:
        for unit in era["units"]:
            recap = unit.get("recapQuiz")
            if recap:
                rid = recap.get("id")
                if rid in recap_ids:
                    errors.append(f"duplicate recapQuiz id {rid}")
                recap_ids.add(rid)
                check_questions(f"unit {unit.get('id')}", recap, 4, 6)
            for a in unit.get("assignments") or []:
                quiz = a.get("quiz")
                if not quiz:
                    continue
                qid = quiz.get("id")
                if qid in quiz_ids:
                    errors.append(f"duplicate quiz id {qid}")
                quiz_ids.add(qid)
                check_questions(a.get("id"), quiz, 3, 5)
    return errors


def apply_tracks(course: dict) -> list[str]:
    errors: list[str] = []
    tracks = (course.get("course") or {}).get("tracks") or []
    index = {}
    for era in course["eras"]:
        for unit in era["units"]:
            for a in unit.get("assignments") or []:
                index[a["id"]] = a
                a.pop("trackIds", None)
    for track in tracks:
        tid = track.get("id")
        if not tid:
            errors.append("track missing id")
            continue
        ids = track.get("assignmentIds") or []
        if not ids:
            errors.append(f"track {tid} has no assignmentIds")
        for aid in ids:
            a = index.get(aid)
            if not a:
                errors.append(f"track {tid}: unknown assignment {aid}")
                continue
            a.setdefault("trackIds", []).append(tid)
    return errors


def main() -> int:
    course = {
        "course": course_meta(),
        "eras": [
            era_presocratic(),
            era_classical(),
            era_hellenistic(),
            era_late_antiquity(),
            era_medieval(),
            era_early_modern(),
            era_empiricism(),
            era_enlightenment(),
            era_nineteenth(),
            era_twentieth_pd(),
            era_present(),
        ],
    }
    report = attach(course)
    errors = apply_thinkers(course)
    errors.extend(apply_assignment_meta(course))
    errors.extend(apply_tracks(course))
    errors.extend(validate_quizzes(course))
    if report["missing_quiz"]:
        errors.append("assignments missing quiz: " + ", ".join(report["missing_quiz"]))
    if report["extra_quiz"]:
        errors.append("quizzes with no assignment: " + ", ".join(report["extra_quiz"]))
    if report["recap_missing_for_large_units"]:
        errors.append(
            "large units missing recapQuiz: " + ", ".join(report["recap_missing_for_large_units"])
        )
    if report["unused_recaps"]:
        errors.append("unused recaps: " + ", ".join(report["unused_recaps"]))

    if errors:
        print("BUILD FAIL", file=sys.stderr)
        for e in errors:
            print(" -", e, file=sys.stderr)
        return 1

    out_content = CONTENT / "course.json"
    out_root = ROOT / "course.json"
    text = json.dumps(course, ensure_ascii=False, indent=2) + "\n"
    out_content.write_text(text, encoding="utf-8")
    out_root.write_text(text, encoding="utf-8")

    n_assign = 0
    n_with = 0
    n_without = 0
    n_recap = 0
    kinds = {"primary": 0, "secondary": 0, "bibliographic": 0}
    with_text = 0
    n_wc = 0
    n_diff = 0
    n_track = 0
    for era in course["eras"]:
        for unit in era["units"]:
            if unit.get("recapQuiz"):
                n_recap += 1
            for a in unit["assignments"]:
                n_assign += 1
                kinds[a.get("kind") or "primary"] = kinds.get(a.get("kind") or "primary", 0) + 1
                if a.get("text"):
                    with_text += 1
                if a.get("quiz"):
                    n_with += 1
                else:
                    n_without += 1
                if a.get("wordCount"):
                    n_wc += 1
                if a.get("difficulty"):
                    n_diff += 1
                if a.get("trackIds"):
                    n_track += 1

    print(f"Wrote {out_content} and {out_root}")
    print(f"eras: {len(course['eras'])}")
    print(f"assignments: {n_assign} (with quiz: {n_with}, without: {n_without})")
    print(f"kinds: {kinds}")
    print(f"assignments with text pointer: {with_text}")
    print(f"with wordCount: {n_wc}; with difficulty: {n_diff}; with trackIds: {n_track}")
    print(f"units with recapQuiz: {n_recap} — {', '.join(report['recap_applied'])}")
    tracks = (course.get("course") or {}).get("tracks") or []
    for t in tracks:
        print(f"track {t.get('id')}: {', '.join(t.get('assignmentIds') or [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
