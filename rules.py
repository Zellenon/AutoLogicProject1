###
# File that implements core rules (e.g. propagate, decide)
###

import copy
import random
from collections import deque

from data_classes import Literal, Reason, State, TruthValue
from utils import (compute_lit_index, exit_sat, exit_unsat,
                   update_watched_literals)


# Decide rule.
# Pick an unassigned literal, give it a random truth value,
# and update our data structures accordingly.
def decide(state: State) -> None:
    # Update model, queue of literals to propagate, and current assignment
    for i in range(len(state.model)):
        if state.model[i] == TruthValue.UNASSIGNED:
            # Guess a value for the ith variable (nondeterministic)
            if random.randint(0, 1) == 0:
                state.to_prop.append((Literal.to_lit(i + 1), Reason.DECIDE, -1))
            else:
                state.to_prop.append((Literal.to_lit(-1 * (i + 1)), Reason.DECIDE, -1))

            # Deterministically choose a value for the ith variable (sometimes better for debugging)
            # state.to_prop.append((Literal.to_lit(i+1), Reason.DECIDE, -1))

            state.decision_level += 1
            return

    # If no variable to decide on, the problem is SAT
    exit_sat(state)


# (Repeated) propagate rule.
# Apply unit propagation to completion (until we exhaust the queue of literals to propagate)
def propagate(state: State) -> None:
    while state.to_prop:
        curr_prop = state.to_prop.popleft()
        curr_lit, curr_reason, curr_clause_index = (
            curr_prop[0],
            curr_prop[1],
            curr_prop[2],
        )

        # Update the current assignment and model with the literal we're propagating
        state.m.append((curr_lit, state.decision_level, curr_reason, curr_clause_index))

        if curr_lit.value:
            if state.model[curr_lit.name - 1] == TruthValue.FALSE:
                conflict(state, curr_clause_index)
                new_decision_level = explain(state)
                backjump(state, new_decision_level)
                return
            else:
                state.model[curr_lit.name - 1] = TruthValue.TRUE
        else:
            if state.model[curr_lit.name - 1] == TruthValue.TRUE:
                conflict(state, curr_clause_index)
                new_decision_level = explain(state)
                backjump(state, new_decision_level)
                return
            else:
                state.model[curr_lit.name - 1] = TruthValue.FALSE

        # Update watched literals of all clauses watching the complement of curr_lit.
        # For these clauses, we either (i) find a new literal to watch, or
        #                              (ii) add the other watched literal to state.to_prop
        curr_lit_comp_index = compute_lit_index(curr_lit.comp())
        watching_clauses = copy.deepcopy(
            state.literals_with_watching_clauses[curr_lit_comp_index][1]
        )
        for clause_index in watching_clauses:
            lit_to_prop = update_watched_literals(
                state, clause_index, state.delta[clause_index - 1], curr_lit.comp()
            )
            # If we cannot find a new literal to watch for some clause,
            # we look at the __other__ watched literal. If it is true, no action is needed.
            # If it is unassigned, we propagate it. If it is false, we have a conflict.
            if lit_to_prop:
                if state.model[lit_to_prop.name - 1] == TruthValue.UNASSIGNED:
                    state.to_prop.append((lit_to_prop, Reason.PROPAGATE, clause_index))
                elif (
                    lit_to_prop.value
                    and state.model[lit_to_prop.name - 1] == TruthValue.FALSE
                ):
                    conflict(state, clause_index)
                    new_decision_level = explain(state)
                    backjump(state, new_decision_level)
                    return
                elif (
                    not lit_to_prop.value
                    and state.model[lit_to_prop.name - 1] == TruthValue.TRUE
                ):
                    conflict(state, clause_index)
                    new_decision_level = explain(state)
                    backjump(state, new_decision_level)
                    return


# (Repeated) explain rule.
# Perform resolution on the conflict clause until we reach a UIP.
# Return the decision level to backjump to.
def explain(state: State) -> int:
    # "Mark" all literals from conflict clause
    marked_lits = set()
    for lit in state.conflict_clause:
        marked_lits.add(lit.comp())

    # We keep applying explain until we find a level to backjump to
    while state.m.tracker:
        top_assign = state.m.tracker[-1]

        # If the top literal in assignment is unmarked, we clear it
        if top_assign[0] not in marked_lits:
            state.m.tracker.pop()
            state.model[top_assign[0].name - 1] = TruthValue.UNASSIGNED
            continue

        # We check if there is another marked literal before the most recent decision.
        # If the current marked literal is a decision, this is trivially true.
        if top_assign[2] == Reason.DECIDE:
            break

        # Otherwise, we search for another marked literal between
        # here and the next decision
        exists_other_marked_lit = False
        for i, assign in reversed(list(enumerate(state.m.tracker[:-1]))):
            if assign[0] in marked_lits:
                exists_other_marked_lit = True
                break
            if state.m.tracker[i][2] == Reason.DECIDE:
                break

        # If not, this is the place we backjump to
        if not exists_other_marked_lit:
            break

        # If so, pop the marked literal and mark its causes
        marked_lits.remove(top_assign[0])
        state.m.tracker.pop()
        state.model[top_assign[0].name - 1] = TruthValue.UNASSIGNED
        for lit in state.delta[top_assign[3] - 1]:
            if lit != top_assign[0]:
                marked_lits.add(lit.comp())

    # If we don't have a decision to flip, fail
    if top_assign[1] == 0:
        exit_unsat()

    # Propagate complement of literal with highest decision level in conflict clause
    state.to_prop = deque(
        [(top_assign[0].comp(), Reason.PROPAGATE, state.num_clauses + 1)]
    )

    # Find next highest decision level
    next_decision_level = 0
    for assign in reversed(state.m.tracker[:-1]):
        if (assign[0] in marked_lits) and (assign[1] < top_assign[1]):
            next_decision_level = assign[1]
            break

    state.decision_level = next_decision_level
    state.conflict_clause = [val.comp() for val in marked_lits]

    # Learn the current conflict clause
    learn(state, top_assign[0])

    return next_decision_level


# Learn rule.
# Add the conflict clause to the clause set delta.
# Also involves initializing watched literals for the new clause.
def learn(state: State, max_dl_lit: Literal) -> None:
    state.num_clauses += 1

    # Add watched literals for conflict clause.
    # First watched literal is the one at highest decision level.
    state.literals_with_watching_clauses[compute_lit_index(max_dl_lit.comp())][
        1
    ].append(state.num_clauses)

    # Move first watched literal to beginning of conflict clause
    max_dl_index = state.conflict_clause.index(max_dl_lit.comp())
    state.conflict_clause[0], state.conflict_clause[max_dl_index] = (
        state.conflict_clause[max_dl_index],
        state.conflict_clause[0],
    )

    # Second watched literal is the second literal of the clause,
    if len(state.conflict_clause) > 1:
        state.literals_with_watching_clauses[
            compute_lit_index(state.conflict_clause[1])
        ][1].append(state.num_clauses)

    # Add conflict clause to clause set
    state.delta.append(state.conflict_clause)
    # print_global_state(state)


# Backjump rule.
# Flip the decision at the decision level prescribed by
# decision_level. Update the assignment and model.
def backjump(state: State, decision_level: int) -> None:
    # Clear conflict clause
    state.conflict_clause = None

    # Clear assignment up to the most recent decision
    while state.m.tracker and state.m.tracker[-1][1] > decision_level:
        state.model[state.m.tracker[-1][0].name - 1] = TruthValue.UNASSIGNED
        state.m.tracker.pop()


# Conflict rule.
# We have reached a conflict, where the clause denoted by
# clause_index is falsified by the current assignment.
# So, we create a conflict clause.
def conflict(state: State, clause_index: int) -> None:
    state.conflict_clause = state.delta[clause_index - 1]
