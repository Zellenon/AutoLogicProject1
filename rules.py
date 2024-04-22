import copy
from typing import Callable

from data_classes import Delta, M, Variable


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


def add_literal(m: M, l: Variable) -> M:
    a = copy.deepcopy(m)
    # a = app_state
    if type(l) == list:
        a.tracker += l
    else:
        a.append(l)
    return a


def match_pure(delta: Delta, m: M) -> bool | None | dict:
    matches = delta.literals
    matches = {
        w
        for w in matches
        if w.inv() not in matches and w not in (m.var_set() | m.inv_set())
    }
    if len(matches) > 0:
        return {"l": min(matches)}
    else:
        return None


def match_propagate(delta: Delta, m: M) -> bool | None | dict:
    for clause in delta.clauses:
        test = clause.vars - m.inv_set()
        if len(test) == 1 and (l := next(iter(test))) not in (
            m.var_set() | m.inv_set()
        ):
            return {"l": l}
    return None


def match_decide(delta: Delta, m: M) -> bool | None | dict:
    options = delta.literals - (m.var_set() | m.inv_set())
    if len(options) > 0:
        decided = min(options)
        return {"l": [decided, None]}
    else:
        return None


def match_backtrack(delta: Delta, m: M) -> bool | None | dict:
    if None in m.tracker:
        index = next(i for i, w in list(enumerate(m.tracker))[::-1] if w == None)
        return {"l": m.tracker[index - 1].inv(), "i": index - 1}


def do_backtrack(m: M, l: Variable, i: int):
    a = copy.deepcopy(m)
    a.tracker = a.tracker[:i] + [l]
    return a


def match_unsat(delta: Delta, m: M) -> bool | None | dict:
    for clause in delta.clauses:
        if clause.vars <= m.inv_set():
            # if False:
            return False
    return None


pure = (match_pure, add_literal)
propagate = (match_propagate, add_literal)
decide = (match_decide, add_literal)
backtrack = (match_backtrack, do_backtrack)

rules: list[tuple[Callable, Callable]] = [
    pure,
    propagate,
    (match_unsat, match_unsat),
    decide,
]
