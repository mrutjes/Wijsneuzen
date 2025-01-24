import os
from code.classes.grid_class import *
from code.imports import *
from code.functions import *
from code.algorithms import *
from code.visualisation.visualisation import *

# Setup

## Get method
iter = get_singular_multiple()

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

## Get sorting method
sort = get_sorting_method(netlist, nodes_list, iter)

## Set variables to keep score of succesfull grids
all_wire_runs = []
successful_grid = 0
tries = 0
cost_min = float('inf')

# Generating solutions

print("Starting algorithm...")

if iter > 1:
    if functie == dfs_algorithm and sort == 'q':
        netlist_new = random.sample(netlist, len(netlist))
        state = state_to_tuple(netlist)
        for h in range(iter):
            i, j = choose_action(state, netlist_new)

            netlist_new[i], netlist_new[j] = netlist_new[j], netlist_new[i]
            next_state = state_to_tuple(netlist)

            grid.clear_wires()
            success = True

            laid_wires = []

            for node1_id, node2_id in netlist_new:
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
                            success = False
                            break        

            if success:
                reward = 1 / grid.cost()
                successful_grid += 1
                if grid.cost() < cost_min:
                    cost_min = grid.cost()
                    wires_cost_min = laid_wires
            else:
                reward = -1
            
            update_q_table(state, (i, j), reward, next_state)
            state = next_state
            tries = h + 1
            print(f"Amount of solutions attempted: {tries}: Best cost so far: {cost_min}")

    elif functie == dfs_algorithm and sort != 'q':
        for netlists in sort:
            grid.clear_wires()

            success = True

            if len(netlists) == 0:
                raise ValueError("No netlist given.")

            laid_wires = []

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
                            success = False
                            break

                if not success:
                    break

            if success:
                all_wire_runs.append(grid._wires)
                successful_grid += 1

                if cost_min > grid.cost():
                    cost_min = grid.cost()
                    wires_cost_min = laid_wires

            tries += 1
            print(f"Amount of solutions attempted: {tries}: Best cost so far: {cost_min}")

            grid.remove_nodes_pointdict()

    elif sort == 'q' and functie != dfs_algorithm:
        for h in range(iter):
            netlist_new = random.sample(netlist, len(netlist))
            state = state_to_tuple(netlist_new)

            i, j = choose_action(state, netlist_new)

            netlist_new[i], netlist_new[j] = netlist_new[j], netlist_new[i]
            next_state = state_to_tuple(netlist_new)

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
                successful_grid += 1
                if grid.cost() < cost_min:
                    cost_min = grid.cost()
                    wires_cost_min = grid._wires
            else:
                reward = -1

            update_q_table(state, (i, j), reward, next_state)
            state = next_state
            tries = h + 1

            print(f"Amount of solutions attempted: {tries}: Best cost so far: {cost_min}")
    else:
        for netlists in sort:
            grid.clear_wires()

            success = True  # a flag we set to false if a route fails

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
                    success = False
                    break  # skip the rest of pairs in this permutation

                # If success, add this wire to the grid's wire list
                grid.add_wire_list(wire)

            # Now we've tried to route all pairs in this permutation (unless we broke early)
            if success:
                # This permutation succeeded for all net pairs
                all_wire_runs.append(grid._wires)
                # If all pairs routed successfully, increment success count
                successful_grid += 1

                if cost_min > grid.cost():
                    cost_min = grid.cost()
                    wires_cost_min = grid._wires
                    working_list = netlists

            tries += 1
            print(f"Amount of solutions attempted: {tries}: Best cost so far: {cost_min}")

            # Optionally remove the nodes from the wire dict
            # (so they don’t appear as intersections, etc.)
            grid.remove_nodes_pointdict()

    # After trying all permutations
    success_percentage = successful_grid / tries * 100
    print(f'{success_percentage}% of the grids were successful')

    # Best solution according to price
    if successful_grid >= 1:
        print(f'The grid with minimal cost costs: {cost_min}')
        plot_wires_3d(wires_cost_min, grid_width, grid_length)

else:
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