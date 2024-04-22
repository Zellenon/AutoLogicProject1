import types
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

    def __or__(self, other, /) -> types.UnionType:
        return Clause(self.vars | other.vars)

    def has_var(self, var: Variable) -> bool:
        return (var in self.vars) or (var.inv() in self.vars)

    def is_sat(self, vars: set[Variable]):
        return len(self.vars & vars) > 0


class M:
    tracker: List[Variable | None]
    var_set: set[Variable]
    inv_set: set[Variable]

    def __init__(self) -> None:
        self.i = False
        self.var_set = set()
        self.inv_set = set()
        self.tracker = []
        self.i = True

    def __setattr__(self, key, value):
        if key == "tracker" and self.i:
            self.var_set = set(self.tracker) - {None}
            self.inv_set = {w.inv() for w in (set(self.tracker) - {None})}
        super(M, self).__setattr__(key, value)

    def append(self, elem: Variable | None):
        self.tracker += [elem]

    def __repr__(self) -> str:
        return str(self.tracker)

    def has_var(self, var: Variable) -> bool:
        return var in self.var_set | self.inv_set


class Delta:
    clauses: list[Clause]

    def __init__(self, clauses: list[Clause]) -> None:
        self.clauses = clauses
        self.literals = {x for xs in clauses for x in xs.vars}

    @classmethod
    def from_string(cls, s):
        return Delta(parse_dimacs(s))

    def __repr__(self) -> str:
        return f"[{', '.join((str(w) for w in self.clauses))}]"

    def is_sat(self, m: M) -> bool:
        return all([w.is_sat(m.var_set) for w in self.clauses])


def parse_dimacs(lines: List[str]) -> list[Clause]:
    delta = []
    for line in lines:
        if line[0] == "c":
            continue
        elif "p cnf" in line:
            pass  # We don't actually need to do anything with this line, right?
        else:
            delta += [
                Clause({Variable.to_var(int(w)) for w in line.split() if int(w) != 0})
            ]
    return delta
