import os
from code.classes.grid_class import *
from code.imports import *
from code.functions import *
from code.algorithms import *
from code.visualisation import *

# Setup

## Get netlist
chip, netlist = get_netlist()

## Get algorithm
functie, algorithm = get_algorithms()

## Create paths
base_path = os.path.join('.', 'gates_netlists')
nodes_csv_path = os.path.join(base_path, f'chip_{chip}', f'print_{chip}.csv')
netlist_csv_path = os.path.join(base_path, f'chip_{chip}', f'netlist_{netlist}.csv')

## Import nodes and netlist
nodes_list = import_nodes(nodes_csv_path)
netlist = import_netlist(netlist_csv_path)

## Initialize grid
grid, grid_width, grid_length = initialise_grid(nodes_list, nodes_csv_path, algorithm, netlist_csv_path)
print(grid.grid_values)

## Get sorting method
sort, iter = get_sorting_method(netlist, nodes_list)

## Set variables to keep score of succesfull grids
all_wire_runs = []
successful_grid = 0
total_tries = 0
cost_min = float('inf')

# Generating solutions

print("Starting algorithm...")

if functie == dfs_algorithm and sort == 'q':
    netlist_new = random.sample(netlist, len(netlist))
    state = state_to_tuple(netlist)
    for tries in range(iter):
        i, j = choose_action(state, netlist_new)

        netlist_new[i], netlist_new[j] = netlist_new[j], netlist_new[i]
        next_state = state_to_tuple(netlist)

        grid.clear_wires()
        success = True

        for node1_id, node2_id in netlist_new:
            node1 = nodes_list[node1_id - 1]
            node2 = nodes_list[node2_id - 1]
            try:
                functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
            except Exception:
                success = False
                break

        if success:
            reward = 1 / grid.cost()
            if grid.cost() < cost_min:
                cost_min = grid.cost()
        else:
            reward = -1

        update_q_table(state, (i, j), reward, next_state)

        state = next_state

        if success:
            successful_grid += 1
            break

        print(f"Amount of solutions attempted: {tries + 1}: Best cost so far: {cost_min}")
elif functie == dfs_algorithm and sort != 'q':
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
elif sort == 'q' and functie != dfs_algorithm:
    for tries in range(iter):  # Aantal iteraties
        # Begin met een willekeurige volgorde
        netlist_new = random.sample(netlist, len(netlist))
        state = state_to_tuple(netlist_new)

        for step in range(50):  # Maximaal aantal stappen per episode
            # Kies een actie (twee items wisselen)
            i, j = choose_action(state, netlist_new)

            # Pas de actie toe
            netlist_new[i], netlist_new[j] = netlist_new[j], netlist_new[i]
            next_state = state_to_tuple(netlist_new)

            # Test de netlist-volgorde
            grid.clear_wires()
            success = True

            for node1_id, node2_id in netlist_new:
                node1 = nodes_list[node1_id - 1]
                node2 = nodes_list[node2_id - 1]
                try:
                    functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                except Exception:
                    success = False
                    break

            # Bereken beloning
            if success:
                reward = 1 / grid.cost()  # Lagere kosten -> hogere beloning
                if grid.cost() < cost_min:
                    cost_min = grid.cost()
            else:
                reward = -1  # Straf voor mislukte volgorde

            # Update de Q-table
            update_q_table(state, (i, j), reward, next_state)

            # Ga naar de volgende staat
            state = next_state

            if success:
                successful_grid += 1
                if cost_min > grid.cost():
                    cost_min = grid.cost()
                    wires_cost_min = laid_wires
                break

        print(f"Amount of solutions attempted: {tries + 1}: Best cost so far: {cost_min}")

    print(f"Q-learning completed. Successful grids: {successful_grid}/{total_tries}")
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

            if cost_min > grid.cost():
                cost_min = grid.cost()
                wires_cost_min = laid_wires
                working_list = netlists

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
    print(working_list)