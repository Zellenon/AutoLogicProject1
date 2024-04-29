###
# File that implements core rules (e.g. propagate, decide)
###

import copy
from collections import deque

from data_classes import State, Literal, TruthValue
from utils import compute_lit_index, update_watched_literals, print_global_state, exit_sat, exit_unsat

# Decide rule. Pick an unassigned literal, give it a random truth value, 
# and update our data structures accordingly.
def decide(state: State) -> None:
    #print("\n----- EXECUTING DECIDE RULE -----\n")

    # Update model, queue of literals to propagate, and current assignment
    for i in range(len(state.model)):
        if (state.model[i] == TruthValue.UNASSIGNED):
            # For now, we are always guessing TRUE initially
            state.to_prop.append(Literal.to_lit(i+1))
            state.decision_level += 1
            #print_global_state(state)
            return

    # If no variable to decide on, the problem is SAT
    exit_sat(state)

# Apply unit propagation to completion (until we exhaust the queue of literals to propagate)
def propagate(state: State) -> None:
    while state.to_prop:
        #print("\n----- EXECUTING PROPAGATE RULE -----\n")
        curr_lit = state.to_prop.popleft()

        # Update the current assignment and model with the literal we're propagating
        state.m.append((curr_lit, state.decision_level))
        if curr_lit.value:
            if state.model[curr_lit.name-1] == TruthValue.FALSE:
                backtrack(state)
            else:
                state.model[curr_lit.name-1] = TruthValue.TRUE
        else:
            if state.model[curr_lit.name-1] == TruthValue.TRUE:
                backtrack(state)
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
                    state.to_prop.append(lit_to_prop)
                elif lit_to_prop.value and state.model[lit_to_prop.name - 1] == TruthValue.FALSE:
                    backtrack(state)
                    return
                elif not lit_to_prop.value and state.model[lit_to_prop.name - 1] == TruthValue.TRUE:
                    backtrack(state)
                    return
                
        #print_global_state(state)
    
# Backtracking function. Update assignment and model.
def backtrack(state: State) -> None:
  #print("\n----- EXECUTING BACKTRACK RULE -----\n")
  state.to_prop = deque()
 
  # Clear assignment up to the most recent decision
  for i, val in reversed(list(enumerate(state.m.tracker))):
    if (i == 0) or (state.m.tracker[i-1][1] != state.decision_level):
      break
    else: 
      state.m.tracker.pop()
      state.model[val[0].name-1] = TruthValue.UNASSIGNED
    
  # If there is no decision to flip, fail
  if state.m.tracker[-1][1] == 0:
    exit_unsat()
    
  # Flip the last decision and update the decision level  
  state.to_prop.append(state.m.tracker[-1][0].comp())
  state.decision_level = state.m.tracker[-1][1] - 1
      
  # Clear last decision from model and state
  state.model[state.m.tracker[-1][0].name-1] = TruthValue.UNASSIGNED
  state.m.tracker.pop()
  
  #print_global_state(state)
