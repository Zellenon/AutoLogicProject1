import sys
from data_classes import parse_dimacs

if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    Delta = parse_dimacs(lines)
    print(Delta)
    print(fname)
