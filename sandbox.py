from enum import Enum
from collections import deque

# TODO: Preprocess unit clauses

input = """p cnf 3 8
-1 -2 -3 0
-1 -2 3 0
-1 2 -3 0
-1 2 3 0
1 -2 -3 0
1 -2 3 0
1 2 -3 0
1 2 3 0"""

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
  print("to_propagate: ", to_propagate)
  print_assignment()
  print("model: ", end="")
  for i, val in enumerate(model, start=1):
    print(i, ": ", val, "; ", end="")
  print()
  print("literals_with_watching_clauses: ", literals_with_watching_clauses)
  print()
  
def preprocess():
  for clause in clauses[1:]:
    if len(clause) == 1:
      to_propagate.append(abs(int(clause[0])))
  
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
  print("----- INITIALIZING GLOBAL STATE -----\n")
  print("input: ", input)
  print("number of variables: ", num_variables)
  print("number of clauses: ", num_clauses) 

  for i in range(1, num_clauses+1):
    if (not input[i][:-1]):
      print("UNSAT")
      exit()
    if (input[i]):
      clauses.append(input[i][:-1])

  print("clauses: ", clauses, end="\n\n")
  
  for i in range(1, num_variables+1):
    model.append(TruthValue.UNASSIGNED)

    watching_clauses_pos = []
    watching_clauses_neg = []

    for j, clause in enumerate(clauses, start=1):
      if (int(clause[0]) == i):
        watching_clauses_pos.append(int(j))
      elif (len(clause) > 1 and int(clause[1]) == i): # TODO: Make more efficient
        watching_clauses_pos.append(int(j))
      elif (int(clause[0]) == -1*i):
        watching_clauses_neg.append(int(j))
      elif (int(len(clause) > 1 and clause[1]) == -1*i): # TODO: Make more efficient
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
      # For now, we are always guessing TRUE initially
      to_propagate.append(i+1)
      decision_level += 1
      print_global_state()
      return
    
  # If no variable to decide on, the problem is SAT
  print("SAT")
  exit()

# We have falsified old_lit (watched by clause) and therefore need to update clause's
# watched literals. We look for another literal to watch. If one exists, we swap it 
# with old_lit and return None. If not, we return the other watch 
# literal (which may spur a conflict or a new propagation).
def update_watched_literals(clause_number, clause, old_lit):
  print("falsified literal:", old_lit)
  print("clause to (attempt to) update:", clause)
  print("clause number:", clause_number)
  if int(clause[0]) == old_lit:
    old_lit_index = 0 
  else:
    old_lit_index = 1

  for i in range(2, len(clause)):
    j = abs(int(clause[i])) - 1
    if (int(clause[i]) > 0 and model[j] != TruthValue.FALSE) or (int(clause[i]) < 0 and model[j] != TruthValue.TRUE):
      
      
      # Update literals_with_watching_clauses. This clause is no longer watching old_lit,
      # and starts watching new_lit
      new_lit = int(clause[i])
      print("new literal to watch:", new_lit, i)
      print("UPDATING literals_with_watching_clauses")
      print(literals_with_watching_clauses)
      literals_with_watching_clauses[compute_lit_index(old_lit)][1].remove(clause_number)
      literals_with_watching_clauses[compute_lit_index(new_lit)][1].append(clause_number)
      print(literals_with_watching_clauses)
      
      clause[old_lit_index], clause[i] = clause[i], clause[old_lit_index]
      print("reordered clause:", clause)
      return None

  # We failed to find a new literal to watch
  try: # This fails for unit clauses
    return int(clause[(old_lit_index + 1) % 2])
  except:
    return old_lit
  
def compute_lit_index(curr_lit):
  if curr_lit > 0:
    return curr_lit * 2 - 2
  else:
    return -1 * curr_lit * 2 - 1

# Apply unit propagation to completion (until we exhaust the queue of literals to propagate)
def propagate():
  while to_propagate:
    print("----- EXECUTING PROPAGATE RULE -----\n")
    curr_lit = to_propagate.popleft()
    
    # Update the current assignment and model with the literal we're propagating
    assignment.append((curr_lit, decision_level))
    if curr_lit > 0:
      if model[curr_lit-1] == TruthValue.FALSE:
        backtrack()
      else:
        model[curr_lit-1] = TruthValue.TRUE
    else:
      if model[-1*curr_lit-1] == TruthValue.TRUE:
        backtrack()
      else:
        model[-1*curr_lit - 1] = TruthValue.FALSE 

    # Update watched literals of all clauses watching the complement of curr_lit.
    # For these clauses, we either (i) find a new literal to watch, or 
    #                              (ii) add the other watched literal to to_propagate
    curr_lit_comp_index = compute_lit_index(-1*curr_lit)
    for clause_index in literals_with_watching_clauses[curr_lit_comp_index][1]: 
      lit_to_prop = update_watched_literals(clause_index, clauses[clause_index-1], -1*curr_lit)
      # If we cannot find a new literal to watch for some clause,
      # we look at the __other__ watched literal. If it is true, no action is needed.
      # If it is unassigned, we propagate it. If it is false, we have a conflict.
      if lit_to_prop:
        if model[abs(lit_to_prop) - 1] == TruthValue.UNASSIGNED:
          to_propagate.append(lit_to_prop)
        elif lit_to_prop > 0 and model[abs(lit_to_prop) - 1] == TruthValue.FALSE:
          backtrack()
          return
        elif lit_to_prop < 0 and model[abs(lit_to_prop) - 1] == TruthValue.TRUE:
          backtrack()
          return
          
    print_global_state()
    
# Backtracking function. Update assignment and model.
# TODO: Debug.
def backtrack():
  print("----- EXECUTING BACKTRACK RULE -----\n")
  global decision_level
  global to_propagate
  
  to_propagate = deque()
 
  # Clear assignment up to the most recent decision
  for i, val in reversed(list(enumerate(assignment))):
    if (i == 0) or (assignment[i-1][1] != decision_level):
      break
    else: 
      assignment.pop()
      model[abs(val[0])-1] = TruthValue.UNASSIGNED
    
  # If there is no decision to flip, fail
  if assignment[-1][1] == 0:
    print("UNSAT")
    exit()
    
  # Flip the last decision and update the decision level  
  assignment[-1] = (-1 * assignment[-1][0], assignment[-1][1] - 1) 
  decision_level = assignment[-1][1]
  if model[abs(assignment[-1][0]) - 1] == TruthValue.TRUE:
    model[abs(assignment[-1][0]) - 1] = TruthValue.FALSE;
  else:
    model[abs(assignment[-1][0]) - 1] = TruthValue.TRUE
    
  # TODO: Update watched literals for flipped literal
  curr_lit = assignment[-1][0]
  curr_lit_index = compute_lit_index(curr_lit)
  for clause_index in literals_with_watching_clauses[curr_lit_index][1]: 
    lit_to_prop = update_watched_literals(clause_index, clauses[clause_index-1], curr_lit)
    
    # If we cannot find a new literal to watch for some clause,
    # we look at the __other__ watched literal. If it is true, no action is needed.
    # If it is unassigned, we propagate it. If it is false, we have a conflict.
    if lit_to_prop:
      if model[abs(lit_to_prop) - 1] == TruthValue.UNASSIGNED:
        to_propagate.append(lit_to_prop)
      elif lit_to_prop > 0 and model[abs(lit_to_prop) - 1] == TruthValue.FALSE:
        backtrack()
        return
      elif lit_to_prop < 0 and model[abs(lit_to_prop) - 1] == TruthValue.TRUE:
        backtrack()
        return
 
def main():    
  initialize_data_structures(input)
  #preprocess()
  while True:
    propagate()
    decide()

main()
