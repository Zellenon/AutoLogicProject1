import sys

from data_classes import AppState
from rules import Sat, Unsat, rules


def do_rules(state: AppState):
    work = True
    applied_rule = True
    while work and applied_rule:
        applied_rule = False
        for rule in rules:
            pre, post = rule
            res = pre(state)
            if type(res) == dict:
                applied_rule = True
                new_state = post(state, **res)
                state = new_state
                print(f"{rule}: {res}")
                break
            elif type(res) == Unsat:
                return Unsat
        print("-----")
        print(state)
    return Sat


if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    state = AppState.from_string(lines)
    print(state)
    print(fname)
    print(state.literals())

    result = do_rules(state)
    print(result)
