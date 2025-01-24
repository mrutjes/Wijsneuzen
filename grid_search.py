import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator, RegressorMixin
from collections import Counter
import os

# You can comment these out or adjust paths/structure if needed.
from code.classes.grid_class import Grid_3D, plot_wires_3d
from code.imports import import_netlist, import_nodes, sort_netlist_busy_nodes, sort_netlist_distance
from code.algorithms import (
    a_star_algorithm,
    manhattan_wire,
    dfs_algorithm,
    lee_algorithm
)
import itertools
from code.classes.wire_class import Wire  # or wherever needed
from code.classes.segment_class import Segment
from code.classes.nodes_class import Node

# Example: define small ranges for each parameter
param_grid = {
    'distance_multiplier':        [0, 1, 2],
    'biggest_1step_cost':         [100, 150, 200],     
    'biggest_2step_cost':         [50, 75, 100],
    'biggest_3step_cost':         [5, 10, 20],
    'big_1step_cost':             [50, 75],
    'big_2step_cost':             [25, 40],
    'big_3step_cost':             [5, 10],
    'medium_1step_cost':          [40, 50],
    'medium_2step_cost':          [15, 30],
    'small_1step_cost':           [25, 40],
}

# For demonstration, let's assume you have:
#  - a function "some_routing_algorithm(grid, netlist)" that tries to lay wires,
#    modifies grid._wires / grid_values, and returns True/False or some measure
#  - or you rely on the grid’s own methods to add wires, etc.

def manual_gridsearch(param_grid, netlist, n=18, m=19, nodes_csv='nodes.csv'):
    """
    Perform a brute-force grid search over the given param_grid.
    Returns the best_param_combination and its cost.
    """
    from itertools import product
    
    # Convert the dict into a list of (key, [values...]) pairs
    param_keys = list(param_grid.keys())
    param_values = list(param_grid.values())
    
    best_score = float('inf')
    best_params = None

    # Iterate over all combinations in Cartesian product
    for combination in product(*param_values):
        # Turn the combination tuple into a dict {param_name: value, ...}
        current_params = dict(zip(param_keys, combination))

        # Instantiate a fresh grid
        grid = Grid_3D(n, m, nodes_csv)

        # 2) Apply the cost-around-nodes with these params
        grid.apply_costs_around_nodes(
            netlist = netlist,
            distance_multiplier   = current_params['distance_multiplier'],
            biggest_1step_cost   = current_params['biggest_1step_cost'],
            biggest_2step_cost   = current_params['biggest_2step_cost'],
            biggest_3step_cost   = current_params['biggest_3step_cost'],
            big_1step_cost       = current_params['big_1step_cost'],
            big_2step_cost       = current_params['big_2step_cost'],
            big_3step_cost       = current_params['big_3step_cost'],
            medium_1step_cost    = current_params['medium_1step_cost'],
            medium_2step_cost    = current_params['medium_2step_cost'],
            small_1step_cost     = current_params['small_1step_cost']
        )

        # 3) Route the netlist (not shown in your snippet):
        #    You probably have some algorithm that tries to lay out wires
        #    using the cost structure in grid.grid_values. For example:
        #
        # success = some_routing_algorithm(grid, netlist, intersection_penalty)
        #
        # That function would place wires in the grid, update grid._wires, etc.
        #
        # For demonstration, let's assume we have it:
        #
        # success = some_routing_algorithm(grid, netlist, intersection_penalty)
        #
        # If it fails or partially completes, we can interpret cost or skip.
        #
        # If no routing code is available, you'll at least have to set wires
        # manually or measure cost in some approximate way.

        # 4) Calculate cost with the grid's .cost() method
        #    (which uses intersection_penalty in part).
        current_cost = grid.cost()

        # Compare to best so far
        if current_cost < best_score:
            best_score = current_cost
            best_params = current_params

    return best_params, best_score


# Example usage:
if __name__ == "__main__":
    # Suppose you’ve loaded or created a netlist
    netlist = [
        # e.g., (nodeA, nodeB), (nodeC, nodeD), ...
        # Must match the type your code expects
    ]

    best_params, best_score = manual_gridsearch(param_grid, netlist)
    print("Best parameters found:", best_params)
    print("Best cost:", best_score)
