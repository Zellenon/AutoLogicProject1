from functools import reduce
from typing import Callable

from data_classes import State, Variable


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


def add_literal(state: State, l: Variable) -> State:
    a = state.copy()
    # a = app_state
    if type(l) == list:
        a.m.tracker += l
    else:
        a.m.append(l)
    return a


def match_pure(state: State) -> bool | None | dict:
    matches = reduce(lambda x, y: x & y, state.delta, set()) - state.m.var_set()
    if len(matches) > 0:
        return {"l": list(matches)}
    else:
        return None


def match_propagate(state: State) -> bool | None | dict:
    for clause in state.delta:
        test = clause - state.m.inv_set()
        if len(test) == 1 and (l := next(iter(test))) not in (
            state.m.var_set() | state.m.inv_set()
        ):
            return {"l": l}
    return None


def match_decide(state: State) -> bool | None | dict:
    options = state.literals - (state.m.var_set() | state.m.inv_set())
    if len(options) > 0:
        decided = min(options)
        return {"l": [decided, None]}
    else:
        return None


def match_backtrack(state: State) -> bool | None | dict:
    if None in state.m.tracker:
        index = next(i for i, w in list(enumerate(state.m.tracker))[::-1] if w == None)
        return {"l": state.m[index - 1].inv(), "i": index - 1}


def do_backtrack(state: State, l: Variable, i: int) -> State:
    a = state.copy()
    a.m.tracker = a.m[:i] + [l]
    return a


def match_unsat(state: State) -> bool | None | dict:
    for clause in state.delta:
        if clause <= state.m.inv_set():
            # if False:
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
