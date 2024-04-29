###
# File with main loop
###
import sys

from tqdm import tqdm

from data_classes import State, parse_dimacs
from rules import propagate, decide


def do_rules(state: State) -> State:
    global pbar 
    pbar = tqdm(total=2 + len({w.name for w in state.m.tracker}))
    while True:
        propagate(state)
        if (not state.to_prop):
            decide(state)
    


if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    state = parse_dimacs(lines)
    #print(state)
    #print(fname)
    do_rules(state)
    pbar.close()
    