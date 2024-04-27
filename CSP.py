from collections import defaultdict, deque


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.arc_trees = defaultdict(dict)  # Store revised values for each variable

    def is_consistent(self, variable, value, assignment):
        for var_i, var_j in self.constraints:
            if var_i == variable and (var_j, value) in assignment.items():
                return False
            if var_j == variable and (var_i, value) in assignment.items():
                return False
        return True

    def arc_consistency(self):
        queue = deque(self.constraints)
        while queue:
            constraint = queue.popleft()
            if self.revise(constraint):
                if len(self.domains[constraint[0]]) == 0:
                    return False  # Inconsistent
                for neighbor in self.get_neighbors(constraint[0]):
                    queue.append((neighbor, constraint[0]))

        return True  # Consistent

    def revise(self, constraint):
        revised = False
        var_i, var_j = constraint
        for value_i in list(self.domains[var_i]):
            if all(
                not self.is_consistent(var_i, value_i, {var_j: value_j})
                for value_j in self.domains[var_j]
            ):
                self.domains[var_i].remove(value_i)
                revised = True
        if revised:
            self.arc_trees[var_i][var_j] = list(
                self.domains[var_i]
            )  # Save revised values
        return revised

    def get_neighbors(self, variable):
        neighbors = []
        for constraint in self.constraints:
            if constraint[0] == variable:
                neighbors.append(constraint[1])
        return neighbors

    def backtracking_search(self, assignment={}):
        if len(assignment) == len(self.variables):
            return assignment  # Solution found
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtracking_search(assignment)
                if result is not None:
                    return result
                del assignment[var]  # Backtrack
        return None  # No solution found

    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var

    def order_domain_values(self, variable, assignment):
        return self.domains[variable]

    def solve(self):
        if not self.arc_consistency():
            return None  # No solution possible due to inconsistency
        return self.backtracking_search()
