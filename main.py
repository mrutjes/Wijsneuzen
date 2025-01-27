import os
import time
import random
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

## Set variables to keep score of successful grids
all_wire_runs = []
successful_grid = 0
tries = 0
cost_min = float('inf')

# Timing setup
total_start_time = time.time()

print("Starting algorithm...")

# -----------------------------------------------------------
# Multiple runs
# -----------------------------------------------------------
if iter > 1:
    # -------------------------------------------------------
    # functie == dfs_algorithm and sort == 'q'
    # -------------------------------------------------------
    if functie == dfs_algorithm and sort == 'q':
        netlist_new = random.sample(netlist, len(netlist))
        state = state_to_tuple(netlist)
        for h in range(iter):
            iteration_start_time = time.time()

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
                            raise Exception(f"No valid path found for net: {node1_id} -> {node2_id}")
                    except Exception:
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

            iteration_end_time = time.time()
            iteration_time = iteration_end_time - iteration_start_time
            print(f"Iteration {h+1} took {iteration_time:.2f} seconds")
            print(f"Amount of solutions attempted: {tries} | Best cost so far: {cost_min}")

    # -------------------------------------------------------
    # functie == dfs_algorithm and sort != 'q'
    # -------------------------------------------------------
    elif functie == dfs_algorithm and sort != 'q':
        for h, netlists in enumerate(sort):
            iteration_start_time = time.time()

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
                        wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                        if wire is not None:
                            laid_wires.append(wire)
                            break
                        else:
                            raise Exception(f"No valid path found for net {i+1}: {node1_id} -> {node2_id}")
                    except Exception:
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
            iteration_end_time = time.time()
            iteration_time = iteration_end_time - iteration_start_time
            print(f"Iteration {h+1} took {iteration_time:.2f} seconds")
            print(f"Amount of solutions attempted: {tries} | Best cost so far: {cost_min}")

            grid.remove_nodes_pointdict()

    # -------------------------------------------------------
    # sort == 'q' and functie != dfs_algorithm
    # -------------------------------------------------------
    elif sort == 'q' and functie != dfs_algorithm:
        for h in range(iter):
            iteration_start_time = time.time()

            netlist_new = random.sample(netlist, len(netlist))
            state = state_to_tuple(netlist_new)

            i, j = choose_action(state, netlist_new)
            netlist_new[i], netlist_new[j] = netlist_new[j], netlist_new[i]
            next_state = state_to_tuple(netlist_new)

            laid_wires = []
            grid.clear_wires()
            grid.apply_costs_around_nodes()

            success = True

            for node1_id, node2_id in netlist_new:
                node1 = nodes_list[node1_id - 1]
                node2 = nodes_list[node2_id - 1]
                try:
                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    laid_wires.append(wire)
                except Exception:
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

            iteration_end_time = time.time()
            iteration_time = iteration_end_time - iteration_start_time
            print(f"Iteration {h+1} took {iteration_time:.2f} seconds")
            print(f"Amount of solutions attempted: {tries} | Best cost so far: {cost_min}")

    # -------------------------------------------------------
    # else scenario for multiple runs
    # -------------------------------------------------------
    else:
        for h, netlists in enumerate(sort):
            iteration_start_time = time.time()

            grid.clear_wires()
            grid.apply_costs_around_nodes()

            success = True

            if len(netlists) == 0:
                raise ValueError("No netlist given.")

            for i in range(len(netlists)):
                node1_id, node2_id = netlists[i]
                node1 = nodes_list[node1_id - 1]
                node2 = nodes_list[node2_id - 1]

                try:
                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    grid.add_wire_list(wire)
                except Exception:
                    success = False
                    break

            if success:
                all_wire_runs.append(grid._wires)
                successful_grid += 1
                if cost_min > grid.cost():
                    cost_min = grid.cost()
                    wires_cost_min = grid._wires
                    working_list = netlists

            tries += 1
            iteration_end_time = time.time()
            iteration_time = iteration_end_time - iteration_start_time
            print(f"Iteration {h+1} took {iteration_time:.2f} seconds")
            print(f"Amount of solutions attempted: {tries} | Best cost so far: {cost_min}")

            grid.remove_nodes_pointdict()

    # After all iterations
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"Total time for {iter} iterations: {total_time:.2f} seconds")

    if tries > 0:
        success_percentage = (successful_grid / tries) * 100
        print(f"{success_percentage}% of the grids were successful")

    if successful_grid >= 1:
        print(f"The grid with minimal cost costs: {cost_min}")
    else:
        print("No successful grid found.")

# -----------------------------------------------------------
# Single run
# -----------------------------------------------------------
else:
    single_run_start_time = time.time()

    # -----------------------------------------------
    # Single run with DFS
    # -----------------------------------------------
    if functie == dfs_algorithm:
        wires = []
        laid_wires = []
        success_for_this_run = True

        if len(netlist) > 0:
            for i, (node1_id, node2_id) in enumerate(netlist):
                node1 = nodes_list[node1_id - 1]
                node2 = nodes_list[node2_id - 1]

                while True:
                    try:
                        wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                        if wire is not None:
                            wires.append(wire)
                            laid_wires.append(wire)
                            break
                        else:
                            raise Exception(f"No valid path found for net {i+1}: {node1_id} -> {node2_id}")
                    except Exception as e:
                        print(e)
                        if laid_wires:
                            last_wire = laid_wires.pop()
                            grid.remove_wire(last_wire)
                        else:
                            success_for_this_run = False
                            print("Backtracking failed, no more wires to remove.")
                            break

                if not success_for_this_run:
                    break

            if success_for_this_run:
                print(f"The total cost for this grid is: {grid.cost()}")
                grid.remove_nodes_pointdict()
            else:
                print("Routing failed for the current netlist.")
        else:
            raise ValueError("No netlist given.")

    # -----------------------------------------------
    # Single run with other algorithms
    # -----------------------------------------------
    else:
        if len(netlist) >= 1:
            wires = grid.return_wire_list()
            for i in range(len(netlist)):
                node1_id, node2_id = netlist[i]
                node1 = nodes_list[node1_id - 1]
                node2 = nodes_list[node2_id - 1]

                wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                grid.add_wire_list(wire)

            print(f"The total cost for this grid is: {grid.cost()}")
            grid.remove_nodes_pointdict()
        else:
            raise ValueError("No netlist given.")

    single_run_end_time = time.time()
    single_run_time = single_run_end_time - single_run_start_time
    print(f"Single run took {single_run_time:.2f} seconds")
