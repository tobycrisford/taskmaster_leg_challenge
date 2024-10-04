import nashpy as nash
import numpy as np

NUMBER_OF_ANIMALS = 6

one_arr = np.ones(NUMBER_OF_ANIMALS)

def payoff_matrix(a_legs: np.ndarray, b_legs: np.ndarray, target: int):

    leg_change = np.outer(one_arr, b_legs) - np.outer(a_legs, one_arr)

    wins = (target - np.sum(a_legs)) == leg_change
    losses = (np.sum(b_legs) - target) == leg_change

    return wins.astype(float) - losses.astype(float)



def solve_game(a_legs: np.ndarray, b_legs: np.ndarray, target: int):

    rps = nash.Game(payoff_matrix(a_legs, b_legs, target))
    return rps.support_enumeration()