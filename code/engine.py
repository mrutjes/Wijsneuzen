import time
import random

from code.functions import state_to_tuple, choose_action, update_q_table
from code.algorithms import dfs_algorithm, manhattan_wire
from code.visualisation.visualisation import plot_wires_3d


def run_multiple_runs(
    iter,
    netlist,
    nodes_list,
    grid,
    cost_min,
    successful_grid,
    tries,
    all_wire_runs,
    nodes_csv_path,
    netlist_csv_path,
    functie, 
    sort
):
    """
    Executes multiple runs of the chosen algorithm.
    Returns:
      (wires_cost_min, successful_grid, tries, cost_min)
    """
    wires_cost_min = None

    if iter > 1:
        
        if functie == dfs_algorithm and sort == 'q':
            netlist_new = random.sample(netlist, len(netlist))
            state = state_to_tuple(netlist)
            for h in range(iter):
                tries += 1
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

                    wire_laid = True
                    while wire_laid:
                        # Find a path
                        wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                        if wire is not None:
                            laid_wires.append(wire)
                            wire_laid = False

                        else:
                            last_wire = laid_wires.pop()
                            grid.remove_wire(last_wire)
                            wire_laid = False

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

                    wire_laid = True
                    while wire_laid:
                        # Find a path
                        wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                        if wire is not None:
                            laid_wires.append(wire)
                            wire_laid = False
                            
                        else:
                            last_wire = laid_wires.pop()
                            grid.remove_wire(last_wire)
                            wire_laid = False

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
        elif sort == 'q' and functie != dfs_algorithm and functie != manhattan_wire:
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
                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    laid_wires.append(wire)
                    if wire is None:
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
        # sort != 'q' and functie == manhattan_wire
        # -------------------------------------------------------
        
        elif sort != 'q' and functie == manhattan_wire:
            for h, netlists in enumerate(sort):
                iteration_start_time = time.time()

                grid.clear_wires()
                grid.apply_costs_around_nodes()

                success = False

                if len(netlists) == 0:
                    raise ValueError("No netlist given.")

                for i in range(len(netlists)):
                    node1_id, node2_id = netlists[i]
                    node1 = nodes_list[node1_id - 1]
                    node2 = nodes_list[node2_id - 1]

                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    grid.add_wire_list(wire)
                
                if grid.failed_wires == 0:
                    success = True

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

        # -------------------------------------------------------
        # sort == 'q' and functie == manhattan_wire
        # -------------------------------------------------------

        elif sort == 'q' and functie == manhattan_wire:
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

                success = False

                for node1_id, node2_id in netlist_new:
                    node1 = nodes_list[node1_id - 1]
                    node2 = nodes_list[node2_id - 1]

                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    laid_wires.append(wire)

                if grid.failed_wires == 0:
                    success = True

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

                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    grid.add_wire_list(wire)

                    if wire is None:
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

    return wires_cost_min, successful_grid, tries, cost_min

def run_single_run(
    functie,
    netlist,
    nodes_list,
    grid,
    grid_width,
    grid_length,
    nodes_csv_path,
    netlist_csv_path
    ):
    """
    Executes a single run of the chosen algorithm.
    """
    # -------------------------------------------------------
    # DFS-algorithm
    # -------------------------------------------------------
    if functie.__name__ == 'dfs_algorithm':

        wires = []
        laid_wires = []
        success_for_this_run = True

        if len(netlist) > 0:
            for i, (node1_id, node2_id) in enumerate(netlist):
                node1 = nodes_list[node1_id - 1]
                node2 = nodes_list[node2_id - 1]
                
                wire_laid = True
                while wire_laid:
                    wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                    if wire is not None:
                        wires.append(wire)
                        laid_wires.append(wire)
                        wire_laid = False

                    if laid_wires:
                        last_wire = laid_wires.pop()
                        grid.remove_wire(last_wire)
                        wire_laid = False

                    else:
                        success_for_this_run = False
                        print("Backtracking failed, no more wires to remove.")
                        break

                if not success_for_this_run:
                    break

            if success_for_this_run:
                print(f"The total cost for this grid is: {grid.cost()}")
                #plot_wires_3d(wires, grid_width, grid_length)
                grid.remove_nodes_pointdict()
            else:
                print("Routing failed for the current netlist.")
        else:
            raise ValueError("No netlist given.")

    # -------------------------------------------------------
    # functie == manhattan_wire
    # -------------------------------------------------------
    elif functie.__name__ == 'manhattan_wire':

        if len(netlist) >= 1:
            wires = grid.return_wire_list()
            for i in range(len(netlist)):
                node1_id, node2_id = netlist[i]
                node1 = nodes_list[node1_id - 1]
                node2 = nodes_list[node2_id - 1]

                wire = functie(node1, node2, grid, nodes_csv_path, netlist_csv_path)
                grid.add_wire_list(wire)
            
            if grid.failed_wires == 0:
                cost_grid = grid.cost()
                print(f"The total cost for this grid is: {cost_grid}")
                #plot_wires_3d(wires, grid_width, grid_length)

            else: 
                print("Routing failed for the current netlist.")
            grid.remove_nodes_pointdict()
        else:
            raise ValueError("No netlist given.")

    # -------------------------------------------------------
    # functie != dfs_algorithm
    # -------------------------------------------------------
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
            #plot_wires_3d(wires, grid_width, grid_length)
            grid.remove_nodes_pointdict()
        else:
            raise ValueError("No netlist given.")
    