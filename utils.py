###
# File that implements helper functions
###
from data_classes import TruthValue, Literal, Clause, State

def compute_lit_index(lit: Literal) -> int:
    if lit.value:
        return lit.name * 2 - 2
    else:
        return lit.name * 2 - 1
    
# We have falsified old_lit (watched by 'clause') and therefore need to update clause's
# watched literals. We look for another literal to watch. If one exists, we swap it 
# with old_lit and return None. If not, we return the other watched 
# literal (which may spur a conflict or a new propagation).
def update_watched_literals(state: State, clause_number: int, clause: Clause, old_lit: Literal) -> Literal | None:
    print("----- UPDATING WATCHED LITERALS -----")
    print("falsified literal:", old_lit)
    print("clause to (attempt to) update:", clause)
    print("clause number:", clause_number)
    if clause[0] == old_lit:
        old_lit_index = 0 
    else:
        old_lit_index = 1

    for i in range(2, len(clause)):
        j = clause[i].name - 1
        if (clause[i].value and state.model[j] != TruthValue.FALSE) or ((not clause[i].value) and state.model[j] != TruthValue.TRUE):
            
            # Update literals_with_watching_clauses. This clause is no longer watching old_lit,
            # and starts watching new_lit
            new_lit = clause[i]
            print("new literal to watch:", new_lit, i)
            print("UPDATING literals_with_watching_clauses")
            lwc = state.literals_with_watching_clauses
            print(lwc[compute_lit_index(old_lit)][1])
            print(lwc[compute_lit_index(new_lit)][1])
            lwc[compute_lit_index(old_lit)][1].remove(clause_number)
            lwc[compute_lit_index(new_lit)][1].append(clause_number)
            print(lwc[compute_lit_index(old_lit)][1])
            print(lwc[compute_lit_index(new_lit)][1])

            clause[old_lit_index], clause[i] = clause[i], clause[old_lit_index]
            print("reordered clause:", clause)
            return None

    # We failed to find a new literal to watch
    try: # This fails for unit clauses
        return clause[(old_lit_index + 1) % 2]
    except: # For unit clauses, we just return the same literal, which will spur a conflict.
        return old_lit
  
def get_decision_level(state: State, lit: Literal) -> int: 
  for asgn in state.m.tracker:
    if (asgn[0] == lit):
      return asgn[1]
    
def print_global_state(state: State) -> None:
  print("----- GLOBAL STATE -----")
  print("to_propagate: ", state.to_prop)
  print("assignment: ", end="")
  for val in state.m.tracker:
    print(f"(literal: {val[0]}, decision_level: {val[1]}, reason: {val[2]}, int: {val[3]}) ", end="")
  print()
  print("model: ", end="")
  for i, val in enumerate(state.model, start=1):
    print(i, ": ", val, "; ", end="")
  print()
  print("literals_with_watching_clauses: ", state.literals_with_watching_clauses)
  print("conflict clause:", state.conflict_clause)
  print("clause set:", state.delta)
  
def exit_sat(state: State):
  print("sat")
  # for i, assignment in enumerate(state.model):
  #   if assignment == TruthValue.TRUE:
  #     truth_value = "true"
  #   else:
  #     truth_value = "false"
  #   print(f"{i+1} := {truth_value}")
  exit()
    
def exit_unsat():
  print("unsat")
  exit()