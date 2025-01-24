import os
from code.classes.grid_class import Grid_3D, plot_wires_3d
from code.imports import *
from code.algorithms import *

# Setup

## Get netlist
while True:
    netlist = input("What netlist do you want to use? Answer must lie between 1-9: ").lower()
    if netlist in {'1', '2', '3'}:
        chip = '0'
        break
    elif netlist in {'4', '5', '6'}:
        chip = '1'
        break
    elif netlist in {'7', '8', '9'}:
        chip = '2'
        break
    else:
        print("Not a valid entry")

## Get algorithm
while True:
    algorithm = input("What algorithm do you want to use? Choose between Manhattan (M), Depth First (D), Lee (L) or A* (A): ").lower()
    if algorithm in {'m', 'manhattan'}:
        functie = manhattan_wire
        break
    elif algorithm in {'d', 'depth first'}:
        functie = dfs_algorithm
        break
    elif algorithm in {'l', 'lee'}:
        functie = lee_algorithm
        break
    elif algorithm in {'a', 'a*'}:
        functie = a_star_algorithm
        break
    else:
        print("Not a valid entry")

## Create paths
base_path = os.path.join('.', 'gates_netlists')
nodes_csv_path = os.path.join(base_path, f'chip_{chip}', f'print_{chip}.csv')
netlist_csv_path = os.path.join(base_path, f'chip_{chip}', f'netlist_{netlist}.csv')


## Import nodes and netlist
nodes_list = import_nodes(nodes_csv_path)
netlist = import_netlist(netlist_csv_path)

## Initialize grid
grid_width = max(node._max_value for node in nodes_list) + 2
grid_length = max(node._max_value for node in nodes_list) + 2
grid = Grid_3D(grid_width, grid_length, nodes_csv_path)
for node in nodes_list:
    grid.place_node(node)

## Get sorting method
while True:
    ans = input("How do you want to sort the netlist? Choose between by: None (N), Busy nodes (B) or Distance of a connection (D): ").lower()
    if ans == 'n' or ans == 'none':
        break
    elif ans == 'd' or ans == 'distance of a connection':
        netlist = sort_netlist_distance(netlist, nodes_list)
        break
    elif ans == 'b' or ans == 'busy nodes':
        netlist = sort_netlist_busy_nodes(netlist)
        break
    else:
        print("Not a valid entry")

## For a* based algorithms, apply costs to certain points
if functie != dfs_algorithm or functie != manhattan_wire:
    netlist_2 = [(nodes_list[x1 - 1], nodes_list[x2 - 1]) for x1, x2 in netlist]
    cost_config = {
    "biggest_ring": {
        "condition": lambda usage, nbrs: (
            usage >= 5
            or (usage >= 4 and nbrs <= 4)
            or (usage >= 3 and nbrs <= 3)
        ),
        "offsets": [
            # 1-step ring with cost=150
            ((0, 0, 1), 150),
            ((0, -1, 0), 150), ((0, 1, 0), 150),
            ((-1, 0, 0), 150), ((1, 0, 0), 150),

            # 2-steps ring with cost=50
            ((0, 0, 2), 50),
            ((0, -2, 0), 50), ((0, 2, 0), 50),
            ((-2, 0, 0), 50), ((2, 0, 0), 50),
            ((-1, -1, 0), 50), ((-1, 1, 0), 50),
            ((1, 1, 0), 50), ((1, -1, 0), 50),
            ((1, 0, 1), 50), ((-1, 0, 1), 50),
            ((0, -1, 1), 50), ((0, 1, 1), 50),

            # 3-steps ring with cost=5
            ((3, 0, 0), 5), ((-3, 0, 0), 5),
            ((0, 3, 0), 5), ((0, -3, 0), 5),
            ((0, 0, 3), 5),
            ((2, 1, 0), 5), ((2, -1, 0), 5), ((2, 0, 1), 5),
            ((-2, 1, 0), 5), ((-2, -1, 0), 5), ((-2, 0, 1), 5),
            ((1, 2, 0), 5), ((1, -2, 0), 5), ((0, 2, 1), 5),
            ((-1, 2, 0), 5), ((-1, -2, 0), 5), ((0, -2, 1), 5),
            ((1, 0, 2), 5), ((-1, 0, 2), 5), ((0, 1, 2), 5), ((0, -1, 2), 5),
            ((1, 1, 1), 5), ((1, -1, 1), 5),
            ((-1, 1, 1), 5), ((-1, -1, 1), 5),
        ]
    },

    "heavy_ring": {
        "condition": lambda usage, nbrs: (
            usage >= 4
            or (usage >= 3 and nbrs <= 4)
            or (usage >= 2 and nbrs <= 3)
        ),
        "offsets": [
            # 1-step ring with cost=50
            ((0, 0, 1), 50),
            ((0, -1, 0), 50), ((0, 1, 0), 50),
            ((-1, 0, 0), 50), ((1, 0, 0), 50),

            # 2-steps ring with cost=25
            ((0, 0, 2), 25),
            ((0, -2, 0), 25), ((0, 2, 0), 25),
            ((-2, 0, 0), 25), ((2, 0, 0), 25),
            ((-1, -1, 0), 25), ((-1, 1, 0), 25),
            ((1, 1, 0), 25), ((1, -1, 0), 25),
            ((1, 0, 1), 25), ((-1, 0, 1), 25),
            ((0, -1, 1), 25), ((0, 1, 1), 25),

            # 3-steps ring with cost=5
            ((3, 0, 0), 5), ((-3, 0, 0), 5),
            ((0, 3, 0), 5), ((0, -3, 0), 5),
            ((0, 0, 3), 5),
            ((2, 1, 0), 5), ((2, -1, 0), 5), ((2, 0, 1), 5),
            ((-2, 1, 0), 5), ((-2, -1, 0), 5), ((-2, 0, 1), 5),
            ((1, 2, 0), 5), ((1, -2, 0), 5), ((0, 2, 1), 5),
            ((-1, 2, 0), 5), ((-1, -2, 0), 5), ((0, -2, 1), 5),
            ((1, 0, 2), 5), ((-1, 0, 2), 5), ((0, 1, 2), 5), ((0, -1, 2), 5),
            ((1, 1, 1), 5), ((1, -1, 1), 5),
            ((-1, 1, 1), 5), ((-1, -1, 1), 5),
        ]
    },

    "medium_ring": {
        "condition": lambda usage, nbrs: (
            usage >= 3
            or (usage >= 2 and nbrs <= 3)
        ),
        "offsets": [
            # 1-step ring with cost=40
            ((0, 0, 1), 40),
            ((0, -1, 0), 40), ((0, 1, 0), 40),
            ((-1, 0, 0), 40), ((1, 0, 0), 40),

            # 2-steps ring with cost=20
            ((0, 0, 2), 20),
            ((0, -2, 0), 20), ((0, 2, 0), 20),
            ((-2, 0, 0), 20), ((2, 0, 0), 20),
            ((-1, -1, 0), 20), ((-1, 1, 0), 20),
            ((1, 1, 0), 20), ((1, -1, 0), 20),
            ((1, 0, 1), 20), ((-1, 0, 1), 20),

            # Notice two special offsets have cost=25
            ((0, -1, 1), 25), ((0, 1, 1), 25),
        ]
    },

    "small_ring": {
        "condition": lambda usage, nbrs: (usage >= 2),
        "offsets": [
            # 1-step ring with cost=30
            ((0, 0, 1), 30),
            ((0, -1, 0), 30), ((0, 1, 0), 30),
            ((-1, 0, 0), 30), ((1, 0, 0), 30),
        ]
    }
}

    grid.apply_costs_around_nodes(netlist=netlist_2, distance_multiplier=2, cost_config=cost_config)


# Laying wires

print("Starting algorithm...")

if functie == dfs_algorithm:
    # Track wires and success
    wires = []
    laid_wires = []  # Track successfully laid wires for potential backtracking
    success_for_this_run = True  # Flag to track the success of the entire run

    if len(netlist) > 0:
        # Loop through the netlist in order (single way)
        for i, (node1_id, node2_id) in enumerate(netlist):
            node1 = nodes_list[node1_id - 1]
            node2 = nodes_list[node2_id - 1]

            while True:
                try:
                    # Attempt to find a route for the current net
                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    if wire is not None:
                        wires.append(wire)  # Store the successfully routed wire
                        laid_wires.append(wire)  # Add to the list of laid wires
                        break  # Exit the while-loop if the wire is successfully routed
                    else:
                        raise Exception(f"No valid path found for net {i+1}: {node1_id} -> {node2_id}")
                except Exception as e:
                    print(e)
                    # Backtrack by removing the last wire
                    if laid_wires:
                        last_wire = laid_wires.pop()  # Remove the last successfully laid wire
                        grid.remove_wire(last_wire)  # Remove it from the grid
                    else:
                        # If no wires to backtrack, mark the run as failed
                        success_for_this_run = False
                        print("Backtracking failed, no more wires to remove.")
                        break

            if not success_for_this_run:
                break  # Stop trying if the entire run is marked as failed

        if success_for_this_run:
            # Calculate and print the cost
            print(f"The total cost for this grid is: {grid.cost()}")

            # Plot the wires
            plot_wires_3d(wires, grid_width, grid_length)

            # Remove the nodes from the wires dictionary
            grid.remove_nodes_pointdict()
        else:
            print("Routing failed for the current netlist.")
    else:
        raise ValueError("No netlist given.")
else:
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

        # Calculate the cost of the grid
        print(f"The total cost for this grid is: {grid.cost()}")

        # Plot the wires
        #plot_wires_3d(wires, grid_width, grid_length)

        # Remove the nodes from the wires dict
        grid.remove_nodes_pointdict()



    else:
        raise ValueError("No netlist given.")