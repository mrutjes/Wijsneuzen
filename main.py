import os
import time

from code.classes.grid_class import initialise_grid
from code.imports import import_netlist, import_nodes
from code.visualisation.visualisation import plot_wires_3d
from code.functions import (
    get_singular_multiple,
    get_netlist,
    get_algorithms,
    get_sorting_method,
)
from code.engine import run_multiple_runs, run_single_run

def main():
    # Setup
    iter = get_singular_multiple()
    chip, netlist = get_netlist()
    functie, algorithm = get_algorithms()

    base_path = os.path.join('.', 'gates_netlists')
    nodes_csv_path = os.path.join(base_path, f'chip_{chip}', f'print_{chip}.csv')
    netlist_csv_path = os.path.join(base_path, f'chip_{chip}', f'netlist_{netlist}.csv')

    nodes_list = import_nodes(nodes_csv_path)
    netlist = import_netlist(netlist_csv_path)

    grid, grid_width, grid_length = initialise_grid(
        nodes_list, 
        nodes_csv_path, 
        algorithm, 
        netlist_csv_path
    )

    # Get sorting method
    sort = get_sorting_method(netlist, nodes_list, iter)

    # Set variables to keep score of successful grids
    all_wire_runs = []
    successful_grid = 0
    tries = 0
    cost_min = float('inf')

    total_start_time = time.time()
    print("Starting algorithm...")

    # -----------------------------------------------------------
    # Multiple runs
    # -----------------------------------------------------------
    if iter > 1:
        # Run multiple iterations
        wires_cost_min, successful_grid, tries, cost_min = run_multiple_runs(
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
        )

        # After all iterations
        total_end_time = time.time()
        total_time = total_end_time - total_start_time
        print(f"Total time for {iter} iterations: {total_time:.2f} seconds")

        if tries > 0:
            success_percentage = (successful_grid / tries) * 100
            print(f"{success_percentage}% of the grids were successful")

        if successful_grid >= 1:
            print(f"The grid with minimal cost costs: {cost_min}")
            plot_wires_3d(wires_cost_min, grid_width, grid_length)
        else:
            print("No successful grid found.")

    # -----------------------------------------------------------
    # Single run
    # -----------------------------------------------------------
    else:
        single_run_start_time = time.time()

        run_single_run(
            functie,
            netlist,
            nodes_list,
            grid,
            grid_width,
            grid_length,
            nodes_csv_path,
            netlist_csv_path,
        )

        single_run_end_time = time.time()
        single_run_time = single_run_end_time - single_run_start_time
        print(f"Single run took {single_run_time:.2f} seconds")

if __name__ == "__main__":
    main()
