from typing import List, Set
import sys

class Variable:
    name: int
    value: bool

    def __init__(self, name: int, value: bool) -> None:
        self.name = name
        self.value = value

    @staticmethod
    def to_var(var: int):
        return Variable(name=abs(var), value=var > 0)

    def __repr__(self) -> str:
        return str(self.name * 1 if self.value else -1)

class Clause:
    vars: Set[Variable]

    def __init__(self, vars: Set[Variable]) -> None:
        self.vars = vars

    def __repr__(self) -> str:
        return "{ " + ", ".join(self.vars) + " }"


def parse_dimacs(lines: List[str]) -> Set[Clause]:
    Delta = set()
    for line in lines:
        if line[0] == 'c':
            continue
        elif 'p cnf' in line:
            pass # We don't actually need to do anything with this line, right?
        else:
            Delta |= {Clause({Variable.to_var(int(w)) for w in line.split()})}
    return Delta

if __name__ == "__main__":
    fname = sys.argv[1]
    lines = open(fname).readlines()
    Delta = parse_dimacs(lines)
    print(Delta)
    print(fname)
