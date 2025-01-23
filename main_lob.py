from code.classes.grid_class import Grid_3D, plot_wires_3d
from code.imports import import_netlist, import_nodes, sort_netlist_busy_nodes, sort_netlist_distance
from code.algorithms import dfs_algorithm as Algorithm

nodes_csv_path = './gates&netlists/chip_0/print_0.csv'
netlist_csv_path = './gates&netlists/chip_0/netlist_1.csv'
functie = Algorithm

# Initiate the grid and nodes
nodes_list = import_nodes(nodes_csv_path)
grid_width = max(node._max_value for node in nodes_list) + 1
grid_length = max(node._max_value for node in nodes_list) + 1
grid = Grid_3D(grid_width, grid_length, nodes_csv_path)

# Place nodes on the grid
for node in nodes_list:
    grid.place_node(node)

# Import the netlist
netlist = import_netlist(netlist_csv_path)
netlist = sort_netlist_busy_nodes(netlist)
netlist = sort_netlist_distance(netlist, nodes_list)

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
        # Plot the wires
        plot_wires_3d(wires, grid_width, grid_length)

        # Remove the nodes from the wires dictionary
        grid.remove_nodes_pointdict()

        # Calculate and print the cost
        total_cost = grid.cost()
        print(f"The total cost for this grid is: {total_cost}")
    else:
        print("Routing failed for the current netlist.")
else:
    raise ValueError("No netlist given.")
