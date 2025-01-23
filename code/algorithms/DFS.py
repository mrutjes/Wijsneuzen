from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
from code.classes.segment_class import Segment

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

    # Loop for laying wire
    while points:
        # Set current point from points list
        current = points.pop()
        x, y, z = current.give_place()

        # Mark as visited
        visited.add(current)

        # If we're next to the end node, finalise this wire
        if grid.distance_nodes(current, WirePoint(x_2, y_2, z_2)) == 1:
            path = []
            while current in parents:
                path.append(current)
                current = parents[current]
            path.reverse()

            # Add ultimate connection to wire
            for point in path:
                wire.add_wire_point(point)

            # Add each segment to the grid
            wirepoints = wire.give_wirepoints()
            for i in range(len(wirepoints) - 1):
                segment = Segment(wirepoints[i], wirepoints[i + 1])
                grid.add_wire_segment(segment)
            final_segment = Segment(wirepoints[-1], WirePoint(x_2, y_2, z_2))
            grid.add_wire_segment(final_segment)

            # Update the grid
            grid.add_wire_dict(wire)
            return wire

        # Else, check surroundings for next step
        surroundings = []
        for x_neighbour, y_neighbour, z_neighbour in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            surrounding = WirePoint(x + x_neighbour, y + y_neighbour, z + z_neighbour)
            segment = Segment(current, surrounding)

            if (surrounding not in visited and grid.check_obstacle(surrounding, segment)):
                surroundings.append(surrounding)

        # Add surroundings to the points and mark their parent
        for surrounding in surroundings:
            if surrounding not in parents:
                parents[surrounding] = current
                points.append(surrounding)

    # If no path is found
    return None
