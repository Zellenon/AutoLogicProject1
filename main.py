import sys

from tqdm import tqdm

from data_classes import M, State, parse_dimacs
from rules import Sat, Unsat, do_backtrack, match_backtrack, rules


def do_rules(state: State) -> State:
    applied_rule = True

    pbar = tqdm(total=2 + len({w.name for w in delta.literals}))
    while applied_rule:
        pbar.set_description(
            f"M: ({len(state.m.tracker)}, {len([w for w in state.m.tracker if w == None])})"
        )
        pbar.update(1)
        applied_rule = False
        for rule in rules:
            pre, post = rule
            res = pre(state)
            if type(res) == dict:
                applied_rule = True
                new_state = post(state, **res)
                # print(f"{pre}: {res}")
                if new_state.is_sat():
                    return new_state
                state = new_state
                # print(f"{m}")
                break
            elif res == False:
                break
        if (res := match_backtrack(state)) and (not applied_rule):
            applied_rule = True
            # print(f"backtrack: {res}")
            state = do_backtrack(state, **res)
            pbar.reset()
            pbar.update(len(state.m.tracker))
        # print("-----")
        # print(m)
    pbar.close()
    return state


if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    delta = State(parse_dimacs(lines))
    print(delta)
    print(fname)

    final_state = do_rules(delta)
    result = Sat() if final_state.is_sat() else Unsat()
    print()
    print(final_state)
    print()
    print(result)
