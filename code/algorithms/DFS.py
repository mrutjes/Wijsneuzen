import pandas as pd
import matplotlib.pyplot as plt
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
from code.classes.segment_class import Segment
import numpy as np

def dfs_algorithm(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str):
    """
    Depth-First Search (DFS) algorithm with backtracking for routing wires.
    """
    wire = Wire(start_node=node1, end_node=node2, nodes_csv_path=nodes_csv_path, netlist_csv_path=netlist_csv_path)
    x_1, y_1, z_1 = node1.give_x(), node1.give_y(), node1.give_z()
    x_2, y_2, z_2 = node2.give_x(), node2.give_y(), node2.give_z()

    points = [WirePoint(x_1, y_1, z_1)]

    # Keep track of visited nodes and parents for backtracking
    visited = set()
    parents = {}

    while points:
        # Set current point from points list
        current = points.pop()
        x, y, z = current.give_place()

        # Mark as visited
        visited.add(current)

        # Check if we are adjacent to the end node
        if grid.distance_nodes(current, WirePoint(x_2, y_2, z_2)) == 1:
            path = []
            while current in parents:
                path.append(current)
                current = parents[current]
            path.reverse()

            # Add the final route into the wire
            for point in path:
                wire.add_wire_point(point)

            # Add each segment to the grid
            wirepoints = wire.give_wirepoints()
            for i in range(len(wirepoints) - 1):
                segment = Segment(wirepoints[i], wirepoints[i + 1])
                grid.add_wire_segment(segment)

            # Add the final segment to the grid
            final_segment = Segment(wirepoints[-1], WirePoint(x_2, y_2, z_2))
            grid.add_wire_segment(final_segment)

            # Update the grid with the wire and return
            grid.add_wire_dict(wire)
            return wire

        # Generate neighbors in all 6 directions
        neighbors = []
        for x_neighbour, y_neighbour, z_neighbour in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            neighbor = WirePoint(x + x_neighbour, y + y_neighbour, z + z_neighbour)
            segment = Segment(current, neighbor)

            # Check if the neighbor is valid, unvisited, and not blocked
            if (neighbor not in visited and
                grid.check_obstacle(neighbor, segment)):
                neighbors.append(neighbor)

        # Add neighbors to the points and mark their parent
        for neighbor in neighbors:
            if neighbor not in parents:
                parents[neighbor] = current
                points.append(neighbor)

    # If no path is found
    return None  # Return None to signal a failure to the main code
