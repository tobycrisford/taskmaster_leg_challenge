from itertools import combinations
import json

import nashpy as nash
import numpy as np

def payoff_matrix(a_legs: np.ndarray, b_legs: np.ndarray, target: int):

    ones_a = np.ones(len(a_legs))
    ones_b = np.ones(len(b_legs))

    leg_change = np.outer(ones_a, b_legs) - np.outer(a_legs, ones_b)

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
                    matrix[i, j] += 1.0
                if b_sum - target == b_throw - a_throw:
                    matrix[i, j] -= 1.0
                else:
                    a_legs[i] = b_throw
                    b_legs[j] = a_throw
                    matrix[i, j] = solve_game_cached(a_legs, b_legs, target, n_rounds - 1)[0]
                    a_legs[i] = a_throw
                    b_legs[j] = b_throw
    else:
        raise NotImplementedError()
    
    rps = nash.Game(matrix)
    for eq in rps.support_enumeration():
        eq_strategy = eq
        break
    return rps[eq_strategy[0], eq_strategy[1]][0], eq_strategy


game_cache = {}

def solve_game_cached(a_legs: np.ndarray, b_legs: np.ndarray, target: int, n_rounds: int):

    a_key = np.sort(a_legs)
    b_key = np.sort(b_legs)
    cache_key = (tuple(a_key), tuple(b_key), target, n_rounds)

    if cache_key not in game_cache:
        new_solution = solve_game(a_legs, b_legs, target, n_rounds)
        # This ensures we store the eq strat in an order invariant way
        strategy = [
            [(a_legs[i], new_solution[1][0][i]) for i in range(len(a_legs))],
            [(b_legs[i], new_solution[1][1][i]) for i in range(len(b_legs))],
        ]
        game_cache[cache_key] = new_solution[0], strategy
    
    return game_cache[cache_key]

def iterate_positions(all_legs: list[int]):
    """Given list of animals, iterate through all possible divisions between players,
    assuming same number on each side.
    """

    all_indices = {i for i in range(len(all_legs))}
    for position in combinations([i for i in range(len(all_legs))], int(len(all_legs) / 2)):
        other_position = all_indices.difference(position)
        a_legs = np.array([all_legs[i] for i in position])
        b_legs = np.array([all_legs[i] for i in other_position])
        yield a_legs, b_legs


def generate_complete_strategy_map(all_legs: list[int], rounds_remaining: int, target: int):

    result = {}
    
    for a_legs, b_legs in iterate_positions(all_legs):
        result_key = tuple(int(a) for a in np.sort(a_legs))
        # Use random shuffling below for more interesting computer strategies (often there are multiple equilibria)
        result[result_key] = solve_game_cached(
            np.random.choice(a_legs, size=len(a_legs), replace=False),
            np.random.choice(b_legs, size=len(b_legs), replace=False),
            target,
            rounds_remaining,
        )

    return result

def clear_cache():

    game_cache = {}

def find_imbalanced_positions(all_legs: list[int], target: int):
    """Return possible situations with asymmetric advantage in a 1-turn game, given list of animals (leg counts).
    
    If empty, then n-turn game strategy will be equivalent to the 1-turn game.
    """

    results = []

    for a_legs, b_legs in iterate_positions(all_legs):
        r = solve_game_cached(a_legs, b_legs, target, 1)
        if r[0] != 0.0:
            results.append((a_legs, b_legs, r[0]))

    return results

def clean_strategy(strat: dict[tuple[int], tuple]):
    """Cleans output of generate_complete_strategy_map for json save."""

    clean_strat = {}
    
    for k in strat:
        a_probs = strat[k][1][0]
        a_probs.sort(key=lambda t: t[0])
        assert all(a_probs[i][0] == k[i] for i in range(len(k)))

        clean_strat[''.join(str(n) for n in k)] = {'value': float(strat[k][0]), 'strategy': [float(a_prob[1]) for a_prob in a_probs]}

    return clean_strat

def save_strategy_map(all_legs: list[int], target: int):
    """Save a strategy map in json format for the indefinite game (just use 10!)"""

    r = generate_complete_strategy_map(all_legs, 10, target)

    filename = ''.join(str(leg) for leg in sorted(all_legs)) + f'_{target}.json'

    with open(filename, 'w') as f:
        json.dump(clean_strategy(r), f)