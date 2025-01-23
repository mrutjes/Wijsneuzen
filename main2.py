import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from code.classes.grid_class import Grid_3D, plot_wires_3d
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
import pandas as pd
from code.imports import import_netlist, import_nodes
from code.algorithms.a_star import a_star_algorithm as Algorithm
import itertools
import csv

nodes_csv_path = './gates&netlists/chip_0/print_0.csv'
netlist_csv_path = './gates&netlists/chip_0/netlist_3.csv'
nodes_list = import_nodes(nodes_csv_path)
grid_width = max(node._max_value for node in nodes_list) + 1
grid_length = max(node._max_value for node in nodes_list) + 1
functie = Algorithm

# Initiate the grid, and import nodes and netlist
grid = Grid_3D(grid_width, grid_length, nodes_csv_path)
nodes_list = import_nodes(nodes_csv_path)
for node in nodes_list:
    grid.place_node(node)
netlist = import_netlist(netlist_csv_path)
all_wire_runs = []
successful_grid = 0
total_tries = 0

for netlists in random_permutations(netlist, 100): # 100 vervangen door hoeveelheid permutaties die je van de netlist wilt
    # Reinitialize the grid for each permutation
    grid.clear_wires()
    wires = grid.return_wire_list()  # empty right now

    success_for_this_permutation = True  # a flag we set to false if a route fails

    if len(netlists) == 0:
        raise ValueError("No netlist given.")

    # Attempt to form wires for each pair in this permutation
    for i in range(len(netlists)):
        node1_id, node2_id = netlists[i]
        node1 = nodes_list[node1_id - 1]
        node2 = nodes_list[node2_id - 1]

        try:
            # Attempt to find a route
            wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
        except Exception as e:
            # If we fail, log it and mark this permutation as failed
            with open('error_log.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([f"Route for pair index {i} in netlist {netlists} failed: {e}"])
            success_for_this_permutation = False
            break  # skip the rest of pairs in this permutation

        # If success, add this wire to the grid's wire list
        grid.add_wire_list(wire)

    # Now we've tried to route all pairs in this permutation (unless we broke early)
    if success_for_this_permutation:
        # This permutation succeeded for all net pairs
        all_wire_runs.append(wires)
        # If all pairs routed successfully, increment success count
        successful_grid += 1

    total_tries += 1

    # Optionally remove the nodes from the wire dict
    # (so they don’t appear as intersections, etc.)
    grid.remove_nodes_pointdict()

# After trying all permutations
success_percentage = (successful_grid / total_tries) * 100
print(f'{success_percentage}% of the grids were successful')
print(f'{successful_grid} out of {total_tries} permutations were successful')