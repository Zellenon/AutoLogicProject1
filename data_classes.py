import copy
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
        return self.name < other.name or (
            self.name == other.name and self.value and not (other.value)
        )

    def __repr__(self) -> str:
        return str(self.name * (1 if self.value else -1))

    def inv(self):
        return Variable(name=self.name, value=not self.value)

    def same_var(self, other) -> bool:
        return self.name == other.name

    @staticmethod
    def to_var(var: int):
        return Variable(name=abs(var), value=var > 0)


class Clause(Set):
    # vars: Set[Variable]

    def __repr__(self) -> str:
        return "{ " + ", ".join({str(w) for w in sorted(list(self))}) + " }"

    def __str__(self) -> str:
        return "{ " + ", ".join({str(w) for w in sorted(list(self))}) + " }"

    def has_var(self, var: Variable) -> bool:
        return (var in self) or (var.inv() in self)

    def is_sat(self, vars: set[Variable]):
        return len(self & vars) > 0

    def inv(self):
        return Clause({w.inv() for w in self})

    def lone(self):
        if len(self) == 1:
            return list(self)[0]
        else:
            return None


class M:
    tracker: List[Variable | None]

    def __init__(self) -> None:
        self.i = False
        self._var_set = Clause()
        self._inv_set = Clause()
        self.tracker = []
        self.old_tracker = []
        self.i = True

    def append(self, elem: Variable | None):
        self.tracker += [elem]

    def __getitem__(self, i):
        return self.tracker[i]

    def __repr__(self) -> str:
        return str(self.tracker)

    def has_var(self, var: Variable) -> bool:
        return var in self.var_set() | self.inv_set()

    def var_set(self) -> Clause:
        if self.tracker == self.old_tracker:
            return self._var_set
        else:
            self.old_tracker = self.tracker.copy()
            self._var_set = Clause(set(self.tracker) - {None})
            self._inv_set = Clause({w.inv() for w in self._var_set})
            return self._var_set

    def inv_set(self) -> Clause:
        if self.tracker == self.old_tracker:
            return self._inv_set
        else:
            self.old_tracker = self.tracker.copy()
            self._var_set = Clause(set(self.tracker) - {None})
            self._inv_set = Clause({w.inv() for w in self._var_set})
            return self._inv_set

    def lev(self, var: Variable):
        var_inv = var.inv()
        index = [i for i, v in enumerate(self.tracker) if v == var or v == var_inv][0]
        return self.tracker[:index].count(None)


class State:
    def __init__(self, delta: list[Clause]) -> None:
        self.delta = delta
        self.m = M()
        self.c: None | Clause = None
        self.to_prop = []
        # self.watched_lits = [(min(w), min(w - {min(w)})) for w in self.delta]
        self.literals = {x for xs in self.delta for x in xs}

    def __repr__(self) -> str:
        strings = [f"Delta: {self.delta}", f"M: {self.m}", f"To Prop: {self.to_prop}"]
        return "\n".join(strings)

    def is_sat(self) -> bool:
        return all([w.is_sat(self.m.var_set()) for w in self.delta])

    def copy(self):
        temp = State(self.delta)
        temp.m = copy.deepcopy(self.m)
        temp.to_prop = copy.deepcopy(self.to_prop)
        temp.c = copy.deepcopy(self.c)
        # temp.watched_lits = copy.deepcopy(self.watched_lits)
        return temp


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
