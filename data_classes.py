###
# File that implements objects representing literals, clauses, and the solver's state
###
from collections import deque
from typing import List, Set, Tuple
from enum import Enum

TruthValue = Enum('TruthValue', ['TRUE', 'FALSE', 'UNASSIGNED'])

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


class Clause(List):
    def __repr__(self) -> str:
        return "[ " + ", ".join({str(w) for w in self}) + " ]"


class M:
    tracker: List[Tuple[Literal, int]]

    def __init__(self) -> None:
        self.tracker = []

    def append(self, elem: Tuple[Literal, int]):
        self.tracker.append(elem)

    def __repr__(self) -> str:
        return str(self.tracker)


class State:
    # State initialization function
    def __init__(self, delta: Set[Clause], num_variables) -> None:
        self.num_variables = num_variables
        self.delta = delta
        self.m = M()
        self.to_prop = deque()
        self.literals = {x for xs in self.delta for x in xs}
        self.model = []
        self.decision_level = 0
        # List of clauses watched by each literal. Each element is a pair.
        # The first item in the pair is the literal, and the second item
        # is the list of clauses that watch the literal. The clauses are not given
        # directly, rather, it is a list of indices of clauses in delta (with 1-based indexing).
        self.literals_with_watching_clauses = []
        
        # Initialize model and watched literals
        for i in range(1, self.num_variables+1):
            self.model.append(TruthValue.UNASSIGNED)

            watching_clauses_pos = []
            watching_clauses_neg = []

            for j, clause in enumerate(list(delta), start=1):
                if (not clause):
                    print("unsat")
                    exit()
                elif (clause[0].name == i and clause[0].value):
                    watching_clauses_pos.append(int(j))
                elif (clause[1:] and clause[1].name == i and clause[1].value):
                    watching_clauses_pos.append(int(j))
                elif (clause[0].name == i and not clause[0].value):
                    watching_clauses_neg.append(int(j))
                elif (clause[1:] and clause[1].name == i and not clause[1].value):
                    watching_clauses_neg.append(int(j))

            self.literals_with_watching_clauses.append((i, watching_clauses_pos))
            self.literals_with_watching_clauses.append((-1*i, watching_clauses_neg))

    def __repr__(self) -> str:
        strings = [f"Delta: {self.delta}", f"M: {self.m}", f"To Prop: {self.to_prop}"]
        return "\n".join(strings)


def parse_dimacs(lines: List[str]) -> List[Clause]:
    delta = []
    for line in lines:
        if line[0] == "c":
            continue
        elif "p cnf" in line:
            num_variables = int(line.split()[3])
        else:
            delta += [
                Clause({Literal.to_lit(int(w)) for w in line.split() if int(w) != 0})
            ]
    return State(delta, num_variables)
