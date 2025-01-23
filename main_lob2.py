from code.classes.grid_class import Grid_3D
from code.imports import import_netlist, import_nodes, random_permutations
from code.algorithms.DFS import dfs_algorithm as Algorithm

nodes_csv_path = './gates&netlists/chip_2/print_2.csv'
netlist_csv_path = './gates&netlists/chip_2/netlist_9.csv'
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

for netlists in random_permutations(netlist, 10): # 100 vervangen door hoeveelheid permutaties die je van de netlist wilt
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

# After trying all permutations
success_percentage = (successful_grid / total_tries) * 100
print(f'{success_percentage}% of the grids were successful')
print(f'{successful_grid} out of {total_tries} permutations were successful')