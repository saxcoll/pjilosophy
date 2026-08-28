"""Merge all assignment quizzes."""
from quizzes_early import all_quizzes as _early
from quizzes_mid import all_quizzes as _mid
from quizzes_late import all_quizzes as _late
from quizzes_recap import all_recaps


def all_quizzes():
    q = {}
    q.update(_early())
    q.update(_mid())
    q.update(_late())
    return q


def recap_quizzes():
    return all_recaps()
