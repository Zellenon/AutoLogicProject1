from functools import reduce
from typing import List, Set


class Variable:
    name: int
    value: bool

    def __init__(self, name: int, value: bool) -> None:
        self.name = abs(name)
        self.value = value

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Variable):
            return self.name == value.name and self.value == value.value
        else:
            return False

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self) -> str:
        return str(self.name * (1 if self.value else -1))

    def inv(self):
        return Variable(name=self.name, value=not self.value)

    def same_var(self, other) -> bool:
        return self.name == other.name

    @staticmethod
    def to_var(var: int):
        return Variable(name=abs(var), value=var > 0)


class Clause:
    vars: Set[Variable]

    def __init__(self, vars: Set[Variable]) -> None:
        self.vars = vars

    def __repr__(self) -> str:
        return "{ " + ", ".join({str(w) for w in self.vars}) + " }"

    def has_var(self, var: Variable) -> bool:
        return (var in self.vars) or (var.inv() in self.vars)

    def is_sat(self, vars: set[Variable]):
        return len(self.vars & vars) > 0


class M:
    tracker: List[Variable | None]

    def __init__(self) -> None:
        self.tracker = []

    def append(self, elem: Variable | None):
        self.tracker += [elem]

    def __repr__(self) -> str:
        return str(self.tracker)

    def has_var(self, var: Variable) -> bool:
        return (var in self.tracker) or (var.inv() in self.tracker)

    def set(self):
        return {w for w in self.tracker if w is not None}


class AppState:
    m: M
    delta: list[Clause]

    def __init__(self, m: M, delta: list[Clause]) -> None:
        self.m = m
        self.delta = delta

    @classmethod
    def from_string(cls, s):
        return AppState(M(), parse_dimacs(s))

    def literals(self):
        return set(reduce(lambda x, y: x | y, [w.vars for w in self.delta]))

    def __repr__(self) -> str:
        return f"C: {self.delta}\nM: {self.m}"

    def is_sat(self) -> bool:
        m = self.m.set()
        return all([w.is_sat(m) for w in self.delta])


def parse_dimacs(lines: List[str]) -> list[Clause]:
    Delta = []
    for line in lines:
        if line[0] == "c":
            continue
        elif "p cnf" in line:
            pass  # We don't actually need to do anything with this line, right?
        else:
            Delta += [
                Clause({Variable.to_var(int(w)) for w in line.split() if int(w) != 0})
            ]
    return Delta
