from enum import Enum

input = "p cnf 3 2\n1 2 -3 0\n-2 3 0"

TruthValue = Enum('TruthValue', ['TRUE', 'FALSE', 'UNASSIGNED'])

# First data structure: queue of literals to propagate
to_propagate = []

# Second data structure: current assignment
assignment = []

# Third data structure: model of current assignment
model = []

# Fourth data structure: list of literals, each pointing to a list of clauses watching that literal
literals_with_watching_clauses = []

# Debug printing function
def print_global_state():
  print("----- GLOBAL STATE -----")
  print("to_propagate: ", to_propagate)
  print("assignment: ", assignment)
  print("model: ", end="")
  for i, val in enumerate(model, start=1):
    print(i, ": ", val, "; ", end="")
  print()
  print("literals_with_watching_clauses: ", literals_with_watching_clauses)
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
  print() 

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
  # Update model, queue of literals to propagate, and current assignment
  for i in range(len(model)):
    if (model[i] == TruthValue.UNASSIGNED):
      model[i] = TruthValue.TRUE
      to_propagate.append(i+1)

      # Increase decision level by 1, starting at 0
      decision_level = 0
      if assignment:
        decision_level = assignment[-1][1] + 1

      assignment.append((i+1, decision_level)) 
      break

initialize_data_structures(input)
print_global_state()
decide()
print_global_state()
