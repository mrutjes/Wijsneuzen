import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from code.classes.grid_class import Grid_3D, plot_wires_3d
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
import pandas as pd
from code.imports import import_netlist, import_nodes
from code.algorithms.manhattan_algorithm import manhattan_wire
import itertools

nodes_csv_path = './gates&netlists/chip_1/print_1.csv'
netlist_csv_path = './gates&netlists/chip_1/netlist_4.csv'
nodes_list = import_nodes(nodes_csv_path)
grid_width = max(node._max_value for node in nodes_list)
grid_length = max(node._max_value for node in nodes_list)
functie = manhattan_wire

# Initiate the grid, and import nodes and netlist
grid = Grid_3D(grid_width, grid_length, nodes_csv_path)
nodes_list = import_nodes(nodes_csv_path)
for node in nodes_list:
    grid.place_node(node)
netlist = import_netlist(netlist_csv_path)
all_wire_runs = []
succesfull_grid = 0
total_tries = 0

for netlists in itertools.permutations(netlist): 
    # Initiate the wires
    grid.clear_wires()
    wires = []
    if len(netlists) >= 1:
        # Form the wires between the nodes based on the given netlist
        wires = grid.return_wire_list()
        for i in range(0, len(netlists)):
            node1 = netlists[i][0]
            node2 = netlists[i][1]

            node1 = nodes_list[node1 - 1]
            node2 = nodes_list[node2 - 1]

            wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)

            grid.add_wire_list(wire)
            
        
        all_wire_runs.append(wires)

        # Calculate the cost of the grid and baseline

        if grid.failed_wires == 0:
            succesfull_grid += 1

        total_tries += 1

        # Plot the wires
        #plot_wires_3d(wires, grid_width, grid_length)

        # Remove the nodes from the wires dict
        grid.remove_nodes_pointdict()

    else:
        raise ValueError("No netlist given.")

succes_percentage = succesfull_grid / total_tries * 100

print(f'{succes_percentage}% of the grids were succesfull')