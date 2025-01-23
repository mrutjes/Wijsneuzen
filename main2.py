from code.classes.grid_class import Grid_3D
from code.imports import *
from code.algorithms import *

while:
    netlist = input("What netlist do you want to use?")
    if netlist >= 1 and netlist <= 3:
        chip = 0
        break
    elif netlist >= 4 and netlist <= 6:
        chip = 1
        break
    elif netlist >= 7 and netlist <= 9:
        chip = 2
        break

# Import paths
nodes_csv_path = './gates&netlists/chip_0/print_0.csv'
netlist_csv_path = './gates&netlists/chip_0/netlist_1.csv'

# Import nodes and netlist
nodes_list = import_nodes(nodes_csv_path)
netlist = import_netlist(netlist_csv_path)

# Initialize grid
grid_width = max(node._max_value for node in nodes_list) + 1
grid_length = max(node._max_value for node in nodes_list) + 1
grid = Grid_3D(grid_width, grid_length, nodes_csv_path)
for node in nodes_list:
    grid.place_node(node)

# -----------------------------------------------------------
# Choose the algorithm you want to use:
# functie = a_star_algorithm
# functie = manhattan_wire
# functie = dfs_algorithm
# functie = lee_algorithm
# -----------------------------------------------------------

# -----------------------------------------------------------
# Choose the sorting method you want to use:
# sort = random_permutations(netlist, 10) # 100 vervangen door hoeveelheid permutaties die je van de netlist wilt
# sort = sort_multiple_netlist_busy_nodes(netlist)
# sort = sort_multiple_netlist_distance(netlist, nodes_list)
# -----------------------------------------------------------

# Set variables to keep score of succesfull grids
all_wire_runs = []
successful_grid = 0
total_tries = 0

# Generating solutions

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

        total_tries += 1
        print(total_tries)

        # Optionally remove the nodes from the wire dict
        grid.remove_nodes_pointdict()
else:
    for netlists in sort:
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