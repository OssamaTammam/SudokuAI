from collections import defaultdict, deque


# Define a class CSP (Constraint Satisfaction Problem)
class CSP:
    # Initialize the CSP object with variables, domains, and constraints
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # List of variables
        self.domains = domains  # Dictionary mapping variables to their domains
        self.constraints = constraints  # List of constraints
        self.arc_trees = defaultdict(dict)  # Store revised values for each variable

    # Check if assigning a value to a variable is consistent with the current assignment
    def is_consistent(self, variable, value, assignment):
        # Check consistency with respect to other variables
        for var_i, var_j in self.constraints:
            if var_i == variable:
                if var_j in assignment and assignment[var_j] == value:
                    return False  # Inconsistent due to value constraint
            elif var_j == variable:
                if var_i in assignment and assignment[var_i] == value:
                    return False  # Inconsistent due to value constraint
        return True

    # Perform arc consistency algorithm
    def arc_consistency(self):
        queue = deque(self.constraints)  # Initialize a queue with constraints
        while queue:
            constraint = queue.popleft()  # Dequeue a constraint
            if self.revise(constraint):  # Perform revise operation
                if len(self.domains[constraint[0]]) == 0:
                    return False  # If domain is empty, inconsistency detected
                for neighbor in self.get_neighbors(constraint[0]):
                    queue.append((neighbor, constraint[0]))  # Add neighbors to queue
        return True  # If no inconsistency detected, return True

    # Revise the domain of a variable based on the given constraint
    def revise(self, constraint):
        revised = False
        var_i, var_j = constraint
        for value_i in list(self.domains[var_i]):  # Iterate over domain of var_i
            if all(
                not self.is_consistent(var_i, value_i, {var_j: value_j})
                for value_j in self.domains[var_j]
            ):
                self.domains[var_i].remove(
                    value_i
                )  # Remove inconsistent value from domain
                revised = True
        if revised:
            self.arc_trees[var_i][var_j] = list(
                self.domains[var_i]
            )  # Save revised values for arc consistency
        return revised

    # Get neighbors of a variable based on constraints
    def get_neighbors(self, variable):
        neighbors = []
        for constraint in self.constraints:
            if constraint[0] == variable:
                neighbors.append(constraint[1])  # Add neighbor to list
        return neighbors

    # Backtracking search algorithm to find a solution
    def backtracking_search(self, assignment={}):
        if len(assignment) == len(self.variables):
            return assignment  # Solution found
        var = self.select_unassigned_variable(assignment)  # Select unassigned variable
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):  # Check consistency
                assignment[var] = value  # Assign value to variable
                result = self.backtracking_search(assignment)  # Recursive call
                if result is not None:
                    return result
                del assignment[var]  # Backtrack if no solution found
        return None  # No solution found

    # Select unassigned variable
    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var

    # Order domain values
    def order_domain_values(self, variable, assignment):
        return self.domains[variable]

    # Solve the CSP problem
    def solve(self):
        if not self.arc_consistency():
            return None  # No solution possible due to inconsistency
        return self.backtracking_search()

    # Print arc consistency information
    def print_arc_trees(self):
        print("Arc Trees:")
        for var_i, neighbor_dict in self.arc_trees.items():
            print(f"Variable {var_i}:")
            for var_j, revised_domain in neighbor_dict.items():
                print(f"  Neighbor variable {var_j}: Revised domain = {revised_domain}")
