from enum import Enum
from collections import deque

# TODO: Preprocess unit clauses
# Q: Do we need to check for conflicts while updating watched literals?
# Q: If not, is it enough to only check watched literals for conflicts?

input = "p cnf 3 2\n1 2 -3 0\n-2 3 0"

TruthValue = Enum('TruthValue', ['TRUE', 'FALSE', 'UNASSIGNED'])

# First data structure: queue of literals to propagate
to_propagate = deque()

# Second data structure: current assignment
assignment = []

# Third data structure: model of current assignment
model = []

# Fourth data structure: list of literals, each pointing to a list of clauses watching that literal
literals_with_watching_clauses = []

# Fifth data structure: set of clauses
clauses = []

decision_level = 0

# Debug printing function
def print_global_state():
  print("----- GLOBAL STATE -----")
  print("to_propagate: ", to_propagate)
  print_assignment()
  print("model: ", end="")
  for i, val in enumerate(model, start=1):
    print(i, ": ", val, "; ", end="")
  print()
  print("literals_with_watching_clauses: ", literals_with_watching_clauses)
  print()
  
def print_assignment():
  print("assignment: ", end="")
  for val in assignment:
    print(f"(literal: {val[0]}, decision_level: {val[1]}) ", end="")
  print()

# Initialization function for our core data structures
def initialize_data_structures(input):
  input = input.split('\n')
  input = [line.split() for line in input]
  num_variables = int(input[0][2])
  num_clauses = int(input[0][3])
  print("----- INITIALIZING GLOBAL STATE -----")
  print("input: ", input)
  print("number of variables: ", num_variables)
  print("number of clauses: ", num_clauses) 

  for i in range(1, num_clauses+1):
    clauses.append(input[i][:-1])

  print("clauses: ", clauses, end="\n\n")

  for i in range(1, num_variables+1):
    model.append(TruthValue.UNASSIGNED)

    watching_clauses_pos = []
    watching_clauses_neg = []

    for j, clause in enumerate(input[1:], start=1):
      if (int(clause[0]) == i):
        watching_clauses_pos.append(int(j))
      elif (int(clause[1]) == i):
        watching_clauses_pos.append(int(j))
      elif (int(clause[0]) == -1*i):
        watching_clauses_neg.append(int(j))
      elif (int(clause[1]) == -1*i):
        watching_clauses_neg.append(int(j))

    literals_with_watching_clauses.append((i, watching_clauses_pos))
    literals_with_watching_clauses.append((-1*i, watching_clauses_neg))

# Decide rule. Pick an unassigned literal, give it a random truth value, 
# and update our data structures accordingly.
def decide():
  print("----- EXECUTING DECIDE RULE -----\n")
  global decision_level
  
  # Update model, queue of literals to propagate, and current assignment
  for i in range(len(model)):
    if (model[i] == TruthValue.UNASSIGNED):
      #model[i] = TruthValue.TRUE
      to_propagate.append(i+1)
      decision_level += 1

      # Increase decision level by 1, starting at 0

      #assignment.append((i+1, get_decision_level() + 1)) 
      break

# We have falsified curr_lit (watched by clause) and therefore need to update clause's
# watched literals. We look for another literal to watch. If one exists, we swap it 
# with curr_lit and return None. If not, we return the other watch 
# literal that now needs to be propagated.
def update_watched_literals(clause, curr_lit):
  if int(clause[0]) == -1*curr_lit:
    old_lit_index = 0 
  else:
    old_lit_index = 1

  for i in range(2, len(clause)):
    if (int(clause[i]) > 0 and model[int(clause[i])-1] != TruthValue.FALSE) or (int(clause[i]) < 0 and model[int(clause[i])-1] != TruthValue.TRUE):
      clause[old_lit_index], clause[i] = clause[i], clause[old_lit_index]
      return None

  return int(clause[(old_lit_index + 1) % 2])


# Apply unit propagation to completion (until we exhaust the queue of literals to propagate)
# TODO: Make sure propagate updates the assignment and model data structures
def propagate():
  while to_propagate:
    print("----- EXECUTING PROPAGATE RULE -----\n")
    curr_lit = to_propagate.popleft()
    
    # Update the current assignment and model with the literal we're propagating
    assignment.append((curr_lit, decision_level))
    if curr_lit > 0:
      model[curr_lit-1] = TruthValue.TRUE
    else:
      model[-1*curr_lit - 1] = TruthValue.FALSE 

    # Update watched literals of all clauses watching the complement of curr_lit.
    # For these clauses, we either (i) find a new literal to watch, or 
    #                              (ii) add the other watched literal to to_propagate
    if curr_lit > 0:
      curr_lit_comp_index = curr_lit * 2 - 1
    else:
      curr_lit_comp_index = curr_lit * 2 - 2
    for clause_index in literals_with_watching_clauses[curr_lit_comp_index][1]: 
      lit_to_prop = update_watched_literals(clauses[clause_index-1], curr_lit)
      if lit_to_prop:
        to_propagate.append(lit_to_prop)
        
    print_global_state()
    
# Backtracking function. Update assignment and model.
def backtrack():
  print("----- APPLYING BACKTRACK RULE -----\n")
  global decision_level
  
  for i, val in reversed(list(enumerate(assignment))):
    # Only undo up to the most recent decision
    if (i == 0) or (assignment[i-1][1] != decision_level):
      break
    else: 
      assignment.pop()
      model[val[1]] = TruthValue.UNASSIGNED
    
  # Flip the last decision and update the decision level
  assignment[-1] = (-1 * assignment[-1][0], assignment[-1][1] - 1) 
  decision_level = assignment[-1][1]
  if model[abs(assignment[-1][0]) - 1] == TruthValue.TRUE:
    model[abs(assignment[-1][0]) - 1] = TruthValue.FALSE;
  else:
    model[abs(assignment[-1][0]) - 1] = TruthValue.TRUE
 
    
initialize_data_structures(input)
print_global_state()
decide()
print_global_state()
propagate()
decide()
print_global_state()
propagate()
backtrack()
print_global_state()
backtrack() 
print_global_state()
