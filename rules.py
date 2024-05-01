###
# File that implements core rules (e.g. propagate, decide)
###

import copy
import random
from collections import deque

from data_classes import State, Literal, TruthValue, Reason
from utils import compute_lit_index, update_watched_literals, print_global_state, exit_sat, exit_unsat, get_decision_level

# Decide rule. 
# Pick an unassigned literal, give it a random truth value, 
# and update our data structures accordingly.
def decide(state: State) -> None:
    print("\n----- EXECUTING DECIDE RULE -----\n")

    # Update model, queue of literals to propagate, and current assignment
    for i in range(len(state.model)):
        if (state.model[i] == TruthValue.UNASSIGNED):
            # Guess a value for the ith variable
            if (random.randint(0, 1) == 0):
                state.to_prop.append((Literal.to_lit(i+1), Reason.DECIDE, -1))
            else:
                state.to_prop.append((Literal.to_lit(-1*(i+1)), Reason.DECIDE, -1))
            state.decision_level += 1
            print_global_state(state)
            return

    # If no variable to decide on, the problem is SAT
    exit_sat(state)

# (Repeated) propagate rule.
# Apply unit propagation to completion (until we exhaust the queue of literals to propagate)
def propagate(state: State) -> None:
    while state.to_prop:
        print("\n----- EXECUTING PROPAGATE RULE -----\n")
        curr_prop = state.to_prop.popleft()
        curr_lit, curr_reason, curr_clause_index = curr_prop[0], curr_prop[1], curr_prop[2]

        # Update the current assignment and model with the literal we're propagating
        state.m.append((curr_lit, state.decision_level, curr_reason, curr_clause_index))
        if curr_lit.value:
            if state.model[curr_lit.name-1] == TruthValue.FALSE:
                conflict(state, curr_clause_index)
                new_decision_level = explain(state)
                backjump(state, new_decision_level)
            else:
                state.model[curr_lit.name-1] = TruthValue.TRUE
        else:
            if state.model[curr_lit.name-1] == TruthValue.TRUE:
                conflict(state, curr_clause_index)
                new_decision_level = explain(state)
                backjump(state, new_decision_level)
            else:
                state.model[curr_lit.name - 1] = TruthValue.FALSE 

        # Update watched literals of all clauses watching the complement of curr_lit.
        # For these clauses, we either (i) find a new literal to watch, or 
        #                              (ii) add the other watched literal to state.to_prop
        curr_lit_comp_index = compute_lit_index(curr_lit.comp())
        watching_clauses = copy.deepcopy(state.literals_with_watching_clauses[curr_lit_comp_index][1])
        for clause_index in watching_clauses: 
            lit_to_prop = update_watched_literals(state, clause_index, state.delta[clause_index-1], curr_lit.comp())
            # If we cannot find a new literal to watch for some clause,
            # we look at the __other__ watched literal. If it is true, no action is needed.
            # If it is unassigned, we propagate it. If it is false, we have a conflict.
            if lit_to_prop:
                if state.model[lit_to_prop.name - 1] == TruthValue.UNASSIGNED:
                    state.to_prop.append((lit_to_prop, Reason.PROPAGATE, clause_index))
                elif lit_to_prop.value and state.model[lit_to_prop.name - 1] == TruthValue.FALSE:
                    conflict(state, curr_clause_index)
                    new_decision_level = explain(state)
                    backjump(state, new_decision_level)
                    return
                elif not lit_to_prop.value and state.model[lit_to_prop.name - 1] == TruthValue.TRUE:
                    conflict(state, curr_clause_index)
                    new_decision_level = explain(state)
                    backjump(state, new_decision_level)
                    return
                
        print_global_state(state)

# (Repeated) explain rule.
# Perform resolution on the conflict clause until we reach a UIP.
# Return the decision level to backjump to.
def explain(state: State) -> int:
    print("\n----- EXECUTING EXPLAIN RULE -----\n")
    print_global_state(state)
    # "Mark" all literals from conflict clause
    marked_lits = set()
    for lit in state.conflict_clause:
        marked_lits.add(lit)
        
    # We keep applying explain until we find a level to backjump to
    while True:
        if not state.m.tracker:
            break
            
        top_assign = state.m.tracker[-1]
        
        # If the top literal in assignment is unmarked, we clear it
        if top_assign[0] not in marked_lits:
            state.m.tracker.pop()
            continue
        
        # We check if there is another marked literal before the most recent decision.
        # If the current marked literal is a decision, this is trivially true.
        if top_assign[2] == Reason.DECIDE:
            break

        # Otherwise, we search for another marked literal between
        # here and the next decision.
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
        for lit in state.delta[top_assign[3]-1]:
            if lit != top_assign[0]:
                marked_lits.add(lit)
                
    learn(state, top_assign[0])
    state.to_prop.append((top_assign[0].comp(), Reason.PROPAGATE, state.num_clauses))
    state.decision_level = top_assign[1] - 1
    return top_assign[1]
        
# Learn rule.
# Add the conflict clause to the clause set delta. 
# Also involves initializing watched literals for the new clause.
def learn(state: State, max_dl_lit: Literal) -> None:
    state.num_clauses += 1
    
    # Add watched literals for conflict clause.
    # First watched literal is the one at highest decision level. 
    state.literals_with_watching_clauses[compute_lit_index(max_dl_lit)][1].append(state.num_clauses)
    
    # Second watched literal is just the first literal of the clause,
    # or the second literal if the first literal is already watched
    if max_dl_lit != state.conflict_clause[0]:
        state.literals_with_watching_clauses[compute_lit_index(state.conflict_clause[0])][1].append(state.num_clauses)
    else:
        state.literals_with_watching_clauses[compute_lit_index(state.conflict_clause[1])][1].append(state.num_clauses)
    
    # Add conflict clause to clause set
    state.delta.append(state.conflict_clause)       
        
# Backjump rule.
# Flip the decision at the decision level prescribed by
# decision_level. Update the assignment and model.
def backjump(state: State, decision_level: int) -> None:
    print("\n----- EXECUTING BACKJUMP RULE -----\n")
    # If there is no decision to flip, fail
    if decision_level == -1:
        exit_unsat()
        
    # Clear conflict clause
    state.conflict_clause = None

    # Clear propagation queue
    state.to_prop = deque()
 
    # Clear assignment up to the most recent decision
    for i, val in reversed(list(enumerate(state.m.tracker))):
        if state.m.tracker[i-1][1] <= decision_level:
            break
        else: 
            state.m.tracker.pop()
            state.model[val[0].name-1] = TruthValue.UNASSIGNED
  
    print_global_state(state)

# Conflict rule.
# We have reached a conflict, where the clause denoted by
# clause_index is falsified by the current assignment.
# So, we create a conflict clause.
def conflict(state: State, clause_index: int) -> None:
    state.conflict_clause = state.delta[clause_index-1]