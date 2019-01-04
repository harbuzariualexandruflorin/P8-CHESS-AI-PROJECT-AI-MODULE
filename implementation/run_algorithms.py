from .algorithms.alfa_beta import alfabeta
from .algorithms.minmax import minmax
from .algorithms.negamax import negamax


DEPTH = 6

states = ['test']  # to be completed later


results = {}
for state in states:
    minmax_result = minmax.min_max_root(DEPTH, state, True)
    alfabeta_result = alfabeta.alpha_beta_root(DEPTH, state, True)
    negamax_result = negamax.negamax_root(DEPTH, state)

    results[state] = (minmax_result, alfabeta_result, negamax_result)


with open('results.txt', 'a') as f:
    for state in results:
        f.write(f'{state}: {results[state][0]} {results[state][1]} {results[state][2]}')
