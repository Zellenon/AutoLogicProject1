import copy
from enum import Enum
from typing import Callable

from data_classes import AppState, Variable


class Sat:
    pass


class Unsat:
    pass


def add_literal(app_state: AppState, l: Variable) -> AppState:
    a = copy.deepcopy(app_state)
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


pure = (match_pure, add_literal)
propagate = (match_propagate, add_literal)

rules: list[tuple[Callable, Callable]] = [pure, propagate]
