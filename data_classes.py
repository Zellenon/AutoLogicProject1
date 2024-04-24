import copy
from typing import List, Set


class Literal:
    name: int
    value: bool

    def __init__(self, name: int, value: bool) -> None:
        self.name = abs(name)
        self.value = value

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Literal):
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

    def comp(self):
        return Literal(name=self.name, value=not self.value)

    def same_lit(self, other) -> bool:
        return self.name == other.name

    @staticmethod
    def to_lit(lit: int):
        return Literal(name=abs(lit), value=lit > 0)


class Clause(Set):
    # lits: Set[Literal]

    def __repr__(self) -> str:
        return "{ " + ", ".join({str(w) for w in self}) + " }"

    def has_var(self, lit: Literal) -> bool:
        return (lit in self) or (lit.comp() in self)

    def is_sat(self, lits: set[Literal]):
        return len(self & lits) > 0


class M:
    tracker: List[Literal | None]

    def __init__(self) -> None:
        self.i = False
        self._lit_set = set()
        self._comp_set = set()
        self.tracker = []
        self.old_tracker = []
        self.i = True

    def append(self, elem: Literal | None):
        self.tracker += [elem]

    def __getitem__(self, i):
        return self.tracker[i]

    def __repr__(self) -> str:
        return str(self.tracker)

    def has_var(self, lit: Literal) -> bool:
        return lit in self.lit_set() | self.comp_set()

    def lit_set(self) -> set[Literal]:
        if self.tracker == self.old_tracker:
            return self._lit_set
        else:
            self.old_tracker = self.tracker.copy()
            self._lit_set = set(self.tracker) - {None}
            self._comp_set = {w.comp() for w in self._lit_set}
            return self._lit_set

    def comp_set(self) -> set[Literal]:
        if self.tracker == self.old_tracker:
            return self._comp_set
        else:
            self.old_tracker = self.tracker.copy()
            self._lit_set = set(self.tracker) - {None}
            self._comp_set = {w.comp() for w in self._lit_set}
            return self._comp_set


class State:
    def __init__(self, delta: list[Clause]) -> None:
        self.delta = delta
        self.m = M()
        self.to_prop = []
        # self.watched_lits = [(min(w), min(w - {min(w)})) for w in self.delta]
        self.literals = {x for xs in self.delta for x in xs}

    def __repr__(self) -> str:
        strings = [f"Delta: {self.delta}", f"M: {self.m}", f"To Prop: {self.to_prop}"]
        return "\n".join(strings)

    def is_sat(self) -> bool:
        return all([w.is_sat(self.m.lit_set()) for w in self.delta])

    def copy(self):
        temp = State(self.delta)
        temp.m = copy.deepcopy(self.m)
        temp.to_prop = copy.deepcopy(self.to_prop)
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
                Clause({Literal.to_lit(int(w)) for w in line.split() if int(w) != 0})
            ]
    return delta
