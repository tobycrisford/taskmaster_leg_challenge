import nashpy as nash
import numpy as np

NUMBER_OF_ANIMALS = 6

one_arr = np.ones(NUMBER_OF_ANIMALS)

def payoff_matrix(a_legs: np.ndarray, b_legs: np.ndarray, target: int):

    leg_change = np.outer(one_arr, b_legs) - np.outer(a_legs, one_arr)

    wins = (target - np.sum(a_legs)) == leg_change
    losses = (np.sum(b_legs) - target) == leg_change

    return wins.astype(float) - losses.astype(float)



def solve_game(a_legs: np.ndarray, b_legs: np.ndarray, target: int, n_rounds: int):

    if n_rounds == 1:
        matrix = payoff_matrix(a_legs, b_legs, target)
    elif n_rounds > 1:
        matrix = np.zeros((len(a_legs), len(b_legs)))
        a_sum = np.sum(a_legs)
        b_sum = np.sum(b_legs)
        for i in range(len(a_legs)):
            for j in range(len(b_legs)):
                a_throw = a_legs[i]
                b_throw = b_legs[j]
                if target - a_sum == b_throw - a_throw:
                    matrix[i, j] = 1.0
                elif b_sum - target == b_throw - a_throw:
                    matrix[i, j] = -1.0
                else:
                    a_legs[i] = b_throw
                    b_legs[j] = a_throw
                    matrix[i, j] = solve_game(a_legs, b_legs, target, n_rounds - 1)[0]
                    a_legs[i] = a_throw
                    b_legs[j] = b_throw
    else:
        raise NotImplementedError()
    
    rps = nash.Game(matrix)
    eq_strategies = list(rps.support_enumeration())
    return rps[eq_strategies[0][0], eq_strategies[0][1]][0], eq_strategies