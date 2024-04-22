import sys

from tqdm import tqdm

from data_classes import AppState
from rules import Sat, Unsat, do_backtrack, match_backtrack, rules


def do_rules(state: AppState) -> AppState:
    work = True
    applied_rule = True

    pbar = tqdm(total=len({w.name for w in state.literals()}))
    while work and applied_rule:
        pbar.reset()
        pbar.update(len(state.m.tracker))
        pbar.set_description(
            f"M: ({len(state.m.tracker)}, {len([w for w in state.m.tracker if w == None])})"
        )
        applied_rule = False
        for rule in rules:
            pre, post = rule
            res = pre(state)
            if type(res) == dict:
                applied_rule = True
                new_state = post(state, **res)
                if new_state.is_sat():
                    return new_state
                state = new_state
                # print(f"{pre}: {res}")
                break
            elif res == False:
                break
        if (res := match_backtrack(state)) and (not applied_rule):
            applied_rule = True
            state = do_backtrack(state, **res)
        # print("-----")
        # print(state)
    pbar.close()
    return state


if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    state = AppState.from_string(lines)
    print(state)
    print(fname)

    state = do_rules(state)
    result = Sat() if state.is_sat() else Unsat()
    print()
    print(state)
    print(result)
