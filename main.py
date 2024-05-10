###
# File with main loop
###
import sys

from data_classes import State, parse_dimacs
from rules import decide, propagate


def solve_clauses(state: State) -> State:
    global pbar
    while True:
        propagate(state)
        if not state.to_prop:
            decide(state)


if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    state = parse_dimacs(lines)
    solve_clauses(state)
