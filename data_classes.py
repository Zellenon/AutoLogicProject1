from typing import List, Set


class Variable:
    name: int
    value: bool

    def __init__(self, name: int, value: bool) -> None:
        self.name = name
        self.value = value

    def __lt__(self, other):
        return abs(self.name) < abs(other.name)

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
        return "{ " + ", ".join({str(w) for w in self.vars}) + " }"


class M:
    tracker: List[Variable | None]

    def append(self, elem: Variable | None):
        self.tracker += [elem]


class AppState:
    m: M
    Delta: Set[Clause]

    def __init__(self, m: M, Delta: Set[Clause]) -> None:
        self.m = m
        self.Delta = Delta

    @classmethod
    def from_string(cls, s):
        return AppState(M(), parse_dimacs(s))


def parse_dimacs(lines: List[str]) -> Set[Clause]:
    Delta = set()
    for line in lines:
        if line[0] == "c":
            continue
        elif "p cnf" in line:
            pass  # We don't actually need to do anything with this line, right?
        else:
            Delta |= {Clause({Variable.to_var(int(w)) for w in line.split()})}
    return Delta
