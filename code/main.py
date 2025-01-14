import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Wijsneuzen.code.classes.grid_class import Grid_3D, plot_wires_3d
from Wijsneuzen.code.classes.nodes_class import Node
from Wijsneuzen.code.classes.wire_class import Wire, WirePoint
import pandas as pd
from imports import import_netlist, import_nodes
from Wijsneuzen.code.algoritms.manhattan_algoritm import manhattan_wire

nodes_csv_path = '../gates&netlists/chip_0/print_0.csv'
netlist_csv_path = '../gates&netlists/chip_0/netlist_1.csv'
grid_width = 10
grid_length = 10
functie = manhattan_wire


# Initiate the grid, and import nodes and netlist
grid = Grid_3D(grid_width, grid_length)
nodes_list = import_nodes(nodes_csv_path)
for node in nodes_list:
    grid.place_node(node)
netlist = import_netlist(netlist_csv_path)

# Initiate the wires
if len(netlist) >= 1:
    # Form the wires between the nodes based on the given netlist
    wires = grid.return_wire_list()
    for i in range(0, len(netlist)):
        node1 = netlist[i][0]
        node2 = netlist[i][1]

        node1 = nodes_list[node1 - 1]
        node2 = nodes_list[node2 - 1]

        wire = functie(node1, node2, grid, nodes_csv_path)

        grid.add_wire_list(wire)

    # Plot the wires
    plot_wires_3d(wires, grid_width, grid_length)

    # Calculate the cost of the grid
    print(f"The total cost for this grid is: {grid.cost()}")
else:
    raise ValueError("No netlist given.")