from enum import Enum
from collections import deque

# TODO: Preprocess unit clauses
# Q: Do we need to check for conflicts while updating watched literals?
# Q: If not, is it enough to only check watched literals for conflicts?

input = """p cnf 60 157
-9 1 0
-9 -2 0
-1 2 9 0
-10 -1 0
-10 2 0
1 -2 10 0
-11 -9 0
-11 -10 0
9 10 11 0
-12 3 0
-12 4 0
-3 -4 12 0
-13 5 0
-13 6 0
-5 -6 13 0
-14 -3 0
-14 -4 0
3 4 14 0
-15 13 0
-15 -14 0
-13 14 15 0
-16 -12 0
-16 -15 0
12 15 16 0
-17 -11 0
-17 -16 0
11 16 17 0
-18 11 0
-18 16 0
-11 -16 18 0
-19 -17 0
-19 -18 0
17 18 19 0
-20 3 0
-20 -4 0
-3 4 20 0
-21 -3 0
-21 4 0
3 -4 21 0
-22 -20 0
-22 -21 0
20 21 22 0
-23 13 0
-23 -22 0
-13 22 23 0
-24 -12 0
-24 -23 0
12 23 24 0
-25 -11 0
-25 -24 0
11 24 25 0
-26 11 0
-26 24 0
-11 -24 26 0
-27 -25 0
-27 -26 0
25 26 27 0
-28 19 0
-28 -27 0
-19 27 28 0
-29 -19 0
-29 27 0
19 -27 29 0
-30 -28 0
-30 -29 0
28 29 30 0
-31 7 0
-31 -8 0
-7 8 31 0
-32 -7 0
-32 8 0
7 -8 32 0
-33 -31 0
-33 -32 0
31 32 33 0
-34 1 0
-34 2 0
-1 -2 34 0
-35 -1 0
-35 -2 0
1 2 35 0
-36 -35 0
-36 -16 0
35 16 36 0
-37 -34 0
-37 -36 0
34 36 37 0
-38 -33 0
-38 -37 0
33 37 38 0
-39 33 0
-39 37 0
-33 -37 39 0
-40 -38 0
-40 -39 0
38 39 40 0
-41 -34 0
-41 -25 0
34 25 41 0
-42 -33 0
-42 -41 0
33 41 42 0
-43 33 0
-43 41 0
-33 -41 43 0
-44 -42 0
-44 -43 0
42 43 44 0
-45 40 0
-45 -44 0
-40 44 45 0
-46 -40 0
-46 44 0
40 -44 46 0
-47 -45 0
-47 -46 0
45 46 47 0
-48 30 0
-48 47 0
-30 -47 48 0
-49 7 0
-49 8 0
-7 -8 49 0
-50 -7 0
-50 -8 0
7 8 50 0
-51 34 0
-51 -50 0
-34 50 51 0
-52 -49 0
-52 -51 0
49 51 52 0
-53 -35 0
-53 -50 0
35 50 53 0
-54 -16 0
-54 53 0
16 -53 54 0
-55 52 0
-55 -54 0
-52 54 55 0
-56 -49 0
-56 -42 0
49 42 56 0
-57 -55 0
-57 56 0
55 -56 57 0
-58 55 0
-58 -56 0
-55 56 58 0
-59 -57 0
-59 -58 0
57 58 59 0
-60 48 0
-60 59 0
-48 -59 60 0
-60 0"""

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
      # For now, we are always guessing TRUE initially
      to_propagate.append(i+1)
      decision_level += 1

      # Increase decision level by 1, starting at 0

      #assignment.append((i+1, get_decision_level() + 1)) 
      print_global_state()
      return
    
  # If no variable to decide on, the problem is SAT
  print("SAT")
  exit()

# We have falsified curr_lit (watched by clause) and therefore need to update clause's
# watched literals. We look for another literal to watch. If one exists, we swap it 
# with curr_lit and return None. If not, we return the other watch 
# literal (which may spur a conflict or a new propagation).
def update_watched_literals(clause, curr_lit):
  if int(clause[0]) == -1*curr_lit:
    old_lit_index = 0 
  else:
    old_lit_index = 1

  for i in range(2, len(clause)):
    j = abs(int(clause[i])) - 1
    if (int(clause[i]) > 0 and model[j] != TruthValue.FALSE) or (int(clause[i]) < 0 and model[j] != TruthValue.TRUE):
      clause[old_lit_index], clause[i] = clause[i], clause[old_lit_index]
      return None

  try: # This fails for unit clauses
    return int(clause[(old_lit_index + 1) % 2])
  except:
    return None


# Apply unit propagation to completion (until we exhaust the queue of literals to propagate)
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
      curr_lit_comp_index = -1 * curr_lit * 2 - 2
    for clause_index in literals_with_watching_clauses[curr_lit_comp_index][1]: 
      lit_to_prop = update_watched_literals(clauses[clause_index-1], curr_lit)
      # If we cannot find a new literal to watch for some clause,
      # we look at the __other__ watched literal. If it is true, no action is needed.
      # If it is unassigned, we propagate it. If it is false, we have a conflict.
      if lit_to_prop:
        if model[abs(lit_to_prop) - 1] == TruthValue.UNASSIGNED:
          to_propagate.append(lit_to_prop)
        elif model[abs(lit_to_prop) - 1] == TruthValue.FALSE:
          backtrack()
          return
          
    print_global_state()
    
# Backtracking function. Update assignment and model.
def backtrack():
  print("----- EXECUTING BACKTRACK RULE -----\n")
  global decision_level
  
  to_propagate = []
 
  # Clear assignment up to the most recent decision
  for i, val in reversed(list(enumerate(assignment))):
    if (i == 0) or (assignment[i-1][1] != decision_level):
      break
    else: 
      assignment.pop()
      model[val[1]] = TruthValue.UNASSIGNED
    
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
 
def main():    
  initialize_data_structures(input)
  #preprocess()
  while True:
    propagate()
    decide()

main()
