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
grid_width = max(node._max_value for node in nodes_list) + 1
grid_length = max(node._max_value for node in nodes_list) + 1
grid = Grid_3D(grid_width, grid_length, nodes_csv_path)
for node in nodes_list:
    grid.place_node(node)

## Get sorting method
while True:
    ans = input("How do you want to sort the netlist? Choose between by: Random (R), Busy nodes (B) or Distance of a connection (D): ").lower()
    if ans == 'r' or ans == 'random':
        ans = input("How many combinations of the netlist do you want to try?: Default is 100. ")
        sort = random_permutations(netlist, int(ans))
        break
    elif ans == 'd' or ans == 'distance of a connection':
        ans = input("How many combinations of the sorted netlist do you want to try?: Default is 100. ")
        sort = sort_multiple_netlist_distance(netlist, nodes_list, int(ans))
        break
    elif ans == 'b' or ans == 'busy nodes':
        ans = input("How many combinations of the sorted netlist do you want to try?: Default is 100.")
        sort = sort_multiple_netlist_busy_nodes(netlist, int(ans))
        break
    else:
        print("Not a valid entry")

## Set variables to keep score of succesfull grids
all_wire_runs = []
successful_grid = 0
total_tries = 0
cost_min = 1000000000


# Generating solutions

print("Starting algorithm...")

if functie == dfs_algorithm:
    for netlists in sort:
        # Reinitialize the grid for each permutation
        grid.clear_wires()
        wires = grid.return_wire_list()

        success_for_this_permutation = True

        if len(netlists) == 0:
            raise ValueError("No netlist given.")

        laid_wires = []

        # Lay wires for this order of the netlist
        for i in range(len(netlists)):
            node1_id, node2_id = netlists[i]
            node1 = nodes_list[node1_id - 1]
            node2 = nodes_list[node2_id - 1]

            while True:
                try:
                    # Find a path
                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    if wire is not None:
                        laid_wires.append(wire)
                        break
                    else:
                        raise Exception(f"No valid path found for net {i+1}: {node1_id} -> {node2_id}")
                except Exception as e:
                    # Backtrack
                    if laid_wires:
                        last_wire = laid_wires.pop()
                        grid.remove_wire(last_wire)
                    else:
                        success_for_this_permutation = False
                        break

            if not success_for_this_permutation:
                break

        # If we're succesfull
        if success_for_this_permutation:
            all_wire_runs.append(wires)
            successful_grid += 1

            if cost_min > grid.cost():
                cost_min = grid.cost()
                wires_cost_min = laid_wires

        total_tries += 1
        print(f"Amount of solutions attempted: {total_tries}")

        # Optionally remove the nodes from the wire dict
        grid.remove_nodes_pointdict()
else:
    for netlists in sort:
        # Reinitialize the grid for each permutation
        grid.clear_wires()
        wires = grid.return_wire_list()  # empty right now

        laid_wires = []

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

            if cost_min > grid.cost():
                cost_min = grid.cost()
                wires_cost_min = laid_wires

        total_tries += 1
        print(f"Amount of solutions attempted: {total_tries}")

        # Optionally remove the nodes from the wire dict
        # (so they don’t appear as intersections, etc.)
        grid.remove_nodes_pointdict()

# After trying all permutations
success_percentage = (successful_grid / total_tries) * 100
print(f'{success_percentage}% of the grids were successful')
print(f'{successful_grid} out of {total_tries} permutations were successful')

# Best solution according to price
if successful_grid >= 1:
    print(f'The grid with minimal cost costs: {cost_min}')
    plot_wires_3d(wires_cost_min, grid_width, grid_length)
