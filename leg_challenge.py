import nashpy as nash
import numpy as np

one_arr = np.ones(6)

def payoff_matrix(a_legs: np.ndarray, b_legs: np.ndarray, target: int):

    leg_change = np.outer(one_arr, b_legs) - np.outer(a_legs, one_arr)

    wins = (target - np.sum(a_legs)) == leg_change
    losses = (np.sum(b_legs) - target) == leg_change

    return wins.astype(float) - losses.astype(float)


