import sys

from tqdm import tqdm

from data_classes import Delta, M
from rules import Sat, Unsat, do_backtrack, match_backtrack, rules


def do_rules(delta: Delta) -> M:
    applied_rule = True

    pbar = tqdm(total=len({w.name for w in delta.literals}))
    m = M()
    while applied_rule:
        pbar.reset()
        pbar.update(len(m.tracker))
        pbar.set_description(
            f"M: ({len(m.tracker)}, {len([w for w in m.tracker if w == None])})"
        )
        applied_rule = False
        for rule in rules:
            pre, post = rule
            res = pre(delta, m)
            if type(res) == dict:
                applied_rule = True
                new_m = post(m, **res)
                print(f"{pre}: {res}")
                if delta.is_sat(new_m):
                    return new_m
                m = new_m
                # print(f"{m}")
                break
            elif res == False:
                break
        if (res := match_backtrack(delta, m)) and (not applied_rule):
            applied_rule = True
            m = do_backtrack(m, **res)
        print("-----")
        print(m)
    pbar.close()
    return m


if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    delta = Delta.from_string(lines)
    print(delta)
    print(fname)

    m = do_rules(delta)
    result = Sat() if delta.is_sat(m) else Unsat()
    print()
    print(m)
    print()
    print(result)
