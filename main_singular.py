from code.classes.grid_class import Grid_3D, plot_wires_3d
from code.imports import *
from code.algorithms import *

# Setup

## Get netlist
while True:
    netlist = input("What netlist do you want to use? Answer must lie between 1-9: ").lower()
    if netlist == '1' or netlist == '2' or netlist == '3':
        chip = '0'
        break
    elif netlist == '4' or netlist == '5' or netlist == '6':
        chip = '1'
        break
    elif netlist == '7' or netlist == '8' or netlist == '9':
        chip = '2'
        break
    else:
        print("Not a valid entry")

## Get algorithm
while True:
    #algorithm = input("What algorithm do you want to use? Choose between Manhattan (M), Depth First (D), Lee (L) or A* (A): ").lower()
    algorithm = 'm' #DIT WEGHALEN
    if algorithm == 'm' or algorithm == 'manhattan':
        functie = manhattan_wire
        break
    elif algorithm == 'd' or algorithm == 'depth first':
        functie = dfs_algorithm
        break
    elif algorithm == 'l' or algorithm == 'lee':
        functie = lee_algorithm
        break
    elif algorithm == 'a' or algorithm == 'a*':
        functie = a_star_algorithm
        break
    else:
        print("Not a valid entry")

## Create paths
nodes_csv_path = './gates&netlists/chip_' + chip + '/print_' + chip + '.csv'
netlist_csv_path = './gates&netlists/chip_' + chip + '/netlist_' + netlist + '.csv'

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
    grid.apply_costs_around_nodes(netlist_2)


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