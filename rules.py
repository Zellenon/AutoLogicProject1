import copy
from enum import Enum
from typing import Callable

from data_classes import AppState, Variable


class Sat:
    def __str__(self) -> str:
        return "Sat"

    def __repr__(self) -> str:
        return "Sat"


class Unsat:
    def __repr__(self) -> str:
        return "Unsat"

    def __str__(self) -> str:
        return "Unsat"


def add_literal(app_state: AppState, l: Variable) -> AppState:
    a = copy.deepcopy(app_state)
    if type(l) == list:
        a.m.tracker += l
    else:
        a.m.append(l)
    return a


def match_pure(app_state: AppState) -> bool | None | dict:
    matches = app_state.literals()
    matches = {
        w
        for w in matches
        if w.inv() not in matches
        and w not in app_state.m.tracker
        and w.inv() not in app_state.m.tracker
    }
    if len(matches) > 0:
        return {"l": min(matches)}
    else:
        return None


def match_propagate(app_state: AppState) -> bool | None | dict:
    for clause in app_state.delta:
        test = clause.vars - {w.inv() for w in app_state.m.tracker if w != None}
        if len(test) == 1 and list(test)[0] not in app_state.m.tracker:
            return {"l": list(test)[0]}
    return None


def match_decide(app_state: AppState) -> bool | None | dict:
    options = app_state.literals() - (
        set(app_state.m.tracker)
        | {w.inv() for w in app_state.m.tracker if w is not None}
    )
    if len(options) > 0:
        decided = min(options)
        return {"l": [decided, None]}
    else:
        return None


def match_backtrack(app_state: AppState) -> bool | None | dict:
    if None in app_state.m.tracker:
        index = next(
            i for i, w in list(enumerate(app_state.m.tracker))[::-1] if w == None
        )
        return {"l": app_state.m.tracker[index - 1].inv(), "i": index - 1}


def do_backtrack(app_state, l: Variable, i: int):
    a = copy.deepcopy(app_state)
    a.m.tracker = a.m.tracker[:i] + [l]
    return a


def match_unsat(app_state) -> bool | None | dict:
    m = app_state.m.set()
    for clause in app_state.delta:
        if {w.inv() for w in clause.vars} <= m:
            return False
    return None


pure = (match_pure, add_literal)
propagate = (match_propagate, add_literal)
decide = (match_decide, add_literal)
backtrack = (match_backtrack, do_backtrack)

rules: list[tuple[Callable, Callable]] = [
    pure,
    (match_unsat, match_unsat),
    propagate,
    decide,
]
