from code.classes.grid_class import Grid_3D, plot_wires_3d
from code.imports import import_netlist, import_nodes
from code.algorithms.algorithms import *

# -----------------------------------------------------------
# Choose the algorithm you want to use:
# functie = a_star_algorithm
# functie = manhattan_wire
# functie = dfs_algorithm
functie = lee_algorithm
# -----------------------------------------------------------

nodes_csv_path = './gates&netlists/chip_0/print_0.csv'
netlist_csv_path = './gates&netlists/chip_0/netlist_1.csv'

# Initiate the grid, and import nodes and netlist
nodes_list = import_nodes(nodes_csv_path)
grid_width = max(node._max_value for node in nodes_list) + 1
grid_length = max(node._max_value for node in nodes_list) + 1
grid = Grid_3D(grid_width, grid_length, nodes_csv_path)
for node in nodes_list:
    grid.place_node(node)
netlist = import_netlist(netlist_csv_path)
# Netlist for apply_costs_around_nodes function
netlist_2 = [(nodes_list[x1 - 1], nodes_list[x2 - 1]) for x1, x2 in netlist]

# Give certain points certain values
grid.apply_costs_around_nodes(netlist_2)
print(f'{grid.grid_values}')

netlist = sort_netlist_busy_nodes(netlist)

# Initiate the wires
if len(netlist) >= 1:
    # Form the wires between the nodes based on the given netlist
    wires = grid.return_wire_list()
    for i in range(0, len(netlist)):
        node1 = netlist[i][0]
        node2 = netlist[i][1]

        node1 = nodes_list[node1 - 1]
        node2 = nodes_list[node2 - 1]

        wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)

        grid.add_wire_list(wire)

    # Plot the wires
    plot_wires_3d(wires, grid_width, grid_length)

    # Remove the nodes from the wires dict
    grid.remove_nodes_pointdict()

    # Calculate the cost of the grid
    print(f"The total cost for this grid is: {grid.cost()}")

else:
    raise ValueError("No netlist given.")