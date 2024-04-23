class BayesianNetwork:
    def __init__(self):
        self.variables = {
            'B': {'parents': [], 'prob_table': {'+b': 0.001, '-b': 0.999}},
            'E': {'parents': [], 'prob_table': {'+e': 0.002, '-e': 0.998}},
            'A': {'parents': ['B', 'E'], 'prob_table': {'+a': {'+b+e': 0.95, '+b-e': 0.94, '-b+e': 0.29, '-b-e': 0.001}, '-a': {'+b+e': 0.05, '+b-e': 0.06, '-b+e': 0.71, '-b-e': 0.999}}},
            'J': {'parents': ['A'], 'prob_table': {'+j': {'+a': 0.9, '-a': 0.05}, '-j': {'+a': 0.1, '-a': 0.95}}},
            'M': {'parents': ['A'], 'prob_table': {'+m': {'+a': 0.7, '-a': 0.01}, '-m': {'+a': 0.3, '-a': 0.99}}}
        }

    def variable_elimination(self, query_variable, evidence):
        factors = self.initialize_factors(evidence)
        order = self.get_elimination_order(query_variable, evidence)
        for var in order:
            factors = self.sum_out(var, factors)
        result = self.normalize(factors[query_variable])
        return result

    def initialize_factors(self, evidence):
        factors = {}
        for var, info in self.variables.items():
            parents = info['parents']
            prob_table = info['prob_table']
            if var in evidence:
                factor = {state: prob_table[state] if state == evidence[var] else 0 for state in prob_table}
            else:
                factor = prob_table.copy()
            factors[var] = factor
        return factors

    def get_elimination_order(self, query_variable, evidence):
        # We can choose any order, a simple strategy is to choose variables not in evidence
        # and not the query variable
        order = [var for var in self.variables if var != query_variable and var not in evidence]
        return order

    def sum_out(self, variable, factors):
        new_factor = {}
        for state in factors[next(iter(factors))]:
            # Select factors that include the variable
            relevant_factors = [factor for var, factor in factors.items() if variable in var]
            # Compute the product of relevant factors
            product = 1
            for factor in relevant_factors:
                if state in factor:
                    product *= factor[state]
            # Sum out the variable
            new_factor[state.replace(variable, '')] = sum(v for k, v in new_factor.items() if k == state.replace(variable, '')) + product
        # Remove old factors and add new factor
        for var in list(factors.keys()):  # Iterate over a copy of keys
            if variable in var:
                del factors[var]
        factors[variable] = new_factor
        return factors

    def normalize(self, factor):
        total = sum(factor.values())
        return {state: prob / total for state, prob in factor.items()}

if __name__ == "__main__":
    bn = BayesianNetwork()
    evidence = {'J': '+j'}
    query_variable = 'B'
    result = bn.variable_elimination(query_variable, evidence)
    print("Probability distribution of Burglary given John Calls = +j:")
    for state, prob in result.items():
        print(f"P({query_variable} = {state} | John Calls = +j) = {prob:.3f}")