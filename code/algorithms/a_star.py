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
    Same as BFS lee's algorithm, except that the distance between nodes is used as a heuristic
    """
    
    wire = Wire(start_node=node1, end_node=node2, nodes_csv_path=nodes_csv_path, netlist_csv_path=netlist_csv_path)
    x_start, y_start, z_start = node1.give_x(), node1.give_y(), node1.give_z()
    x_end, y_end, z_end = node2.give_x(), node2.give_y(), node2.give_z()

    # Priority queue for A* (min-heap)
    q = []
    heapq.heappush(q, (0, WirePoint(x_start, y_start, z_start)))

    # Dictionary to track cumulative costs and parents
    costs = {WirePoint(x_start, y_start, z_start): 0}
    parents = {}

    # Set to track visited segments (current_point, neighbor_point)
    visited_segments = set()

    while q:
        current_f_cost, current = heapq.heappop(q)
        x, y, z = current.give_place()

        # Check if we have reached the endpoint
        if current.give_place() == (x_end, y_end, z_end):
            print("Endpoint reached")
            # Reconstruct the path
            path = []
            while current in parents:
                path.append(current)
                current = parents[current]
            path.reverse()
            for point in path:
                wire.add_wire_point(point)

            return wire

        neighbors = []
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            temp_wirepoint = WirePoint(x + dx, y + dy, z + dz)
            temp_segment = Segment(current, temp_wirepoint)

            # Validate the neighbor and segment
            if (
                grid.check_obstacle(temp_wirepoint, temp_segment)
                and (current, temp_wirepoint) not in visited_segments
            ):
                neighbors.append(temp_wirepoint)

        for neighbor in neighbors:
            crossing_penalty = 300 if grid.is_crossing(neighbor) else 0
            layer_change_penalty = 1 if current.give_z() != neighbor.give_z() else 0
            g_cost = costs[current] + grid.cost_point(neighbor) + crossing_penalty + layer_change_penalty
            # Use the grid's distance_nodes method for the heuristic
            h_cost = grid.distance_nodes(neighbor, WirePoint(x_end, y_end, z_end))
            f_cost = g_cost + h_cost

            # Ensure continuity and no returns
            if g_cost < costs.get(neighbor, float('inf')):
                costs[neighbor] = g_cost
                parents[neighbor] = current
                visited_segments.add((current, neighbor))  # Mark the segment as visited
                heapq.heappush(q, (f_cost, neighbor))

    # If the loop exits without connecting the nodes
    raise Exception("No valid path found between the nodes.")
