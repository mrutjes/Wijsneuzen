import pandas as pd
import matplotlib.pyplot as plt
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
import numpy as np
import heapq
from code.classes.segment_class import Segment

def a_star_algorithm(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str):
    """
    Same as BFS/Lee's algorithm, except that we use an A* approach:
    we combine the actual distance traveled (g_cost) with a heuristic (h_cost).
    """

    wire = Wire(start_node=node1, end_node=node2,
                nodes_csv_path=nodes_csv_path, netlist_csv_path=netlist_csv_path)
    x_start, y_start, z_start = node1.give_x(), node1.give_y(), node1.give_z()
    x_end,   y_end,   z_end   = node2.give_x(), node2.give_y(), node2.give_z()

    # Priority queue for A* (min-heap of (f_cost, WirePoint))
    q = []
    start_point = WirePoint(x_start, y_start, z_start)
    heapq.heappush(q, (0, start_point))

    # Keep track of g_cost (distance so far) and parents for path reconstruction
    costs = {start_point: 0}
    parents = {}

    # Standard A* closed set of already-processed nodes
    closed_set = set()

    while q:
        current_f_cost, current = heapq.heappop(q)
        x, y, z = current.give_place()

        # If we've already processed this node at its best cost, skip
        if current in closed_set:
            continue
        closed_set.add(current)

        # Check if we've reached a point adjacent to the end (distance == 1)
        point_dict = grid.return_point_dict()
        if (grid.distance_nodes(current, WirePoint(x_end, y_end, z_end)) == 1 and point_dict[current.give_place()] == 0):
            # Reconstruct the path by backtracking through parents
            path = []
            while current in parents:
                path.append(current)
                current = parents[current]
            path.reverse()

            # Now add the final route into the wire
            for point in path:
                wire.add_wire_point(point)

            # After final route is known, add each segment to the grid
            wirepoints = wire.give_wirepoints()
            for i in range(len(wirepoints) - 1):
                segment = Segment(wirepoints[i], wirepoints[i + 1])
                grid.add_wire_segment(segment)  # Mark the segment as occupied
            
            # Also add the final segment to the grid
            node_point = WirePoint(node2.give_x(), node2.give_y(), node2.give_z())
            final_segment = Segment(wirepoints[-1], node_point)
            grid.add_wire_segment(final_segment)
            
            # Return wire and add to dict to update cost calculations
            grid.add_wire_dict(wire)
            return wire

        # Generate neighbors in 6 directions
        neighbors = []
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0),
                           (0, -1, 0), (0, 1, 0),
                           (0, 0, -1), (0, 0, 1)]:
            temp_wirepoint = WirePoint(x + dx, y + dy, z + dz)
            temp_segment = Segment(current, temp_wirepoint)

            # Only add neighbor if it's a valid, unblocked cell
            if grid.check_obstacle(temp_wirepoint, temp_segment):
                neighbors.append(temp_wirepoint)

        # Evaluate each neighbor
        for neighbor in neighbors:
            if neighbor in closed_set:
                continue

            # Compute g_cost (distance so far) + h_cost (heuristic)
            print(grid.cost_point(neighbor))
            g_cost = costs[current] + grid.get_point_value(neighbor) + grid.cost_point(neighbor)
            h_cost = grid.distance_nodes(neighbor, WirePoint(x_end, y_end, z_end))
            f_cost = g_cost + h_cost

            # If this new route to neighbor is cheaper, update
            if g_cost < costs.get(neighbor, float('inf')):
                costs[neighbor] = g_cost
                parents[neighbor] = current
                heapq.heappush(q, (f_cost, neighbor))

    # If the priority queue empties out and we never found a path:
    raise Exception("No valid path found between the nodes.")
