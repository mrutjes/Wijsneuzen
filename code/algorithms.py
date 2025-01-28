from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
from code.classes.segment_class import Segment
import heapq


def a_star_algorithm(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str) -> Wire|None:
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
            grid.set_point_value(wire, 50) # The penalty for intersections tuned during experimental phase
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
            g_cost = costs[current] + grid.get_point_value(neighbor)
            h_cost = grid.distance_nodes(neighbor, WirePoint(x_end, y_end, z_end))
            f_cost = g_cost + h_cost

            # If this new route to neighbor is cheaper, update
            if g_cost < costs.get(neighbor, float('inf')):
                costs[neighbor] = g_cost
                parents[neighbor] = current
                heapq.heappush(q, (f_cost, neighbor))

    # If the priority queue empties out and we never found a path:
    return None


def lee_algorithm(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str) -> Wire|None:
    """
    Breath first search with applied cost function. Works the same as the a* algorithm, except
    that it does not use a heuristic.
    """

    wire = Wire(start_node=node1, end_node=node2,
                nodes_csv_path=nodes_csv_path, netlist_csv_path=netlist_csv_path)
    x_start, y_start, z_start = node1.give_x(), node1.give_y(), node1.give_z()
    x_end,   y_end,   z_end   = node2.give_x(), node2.give_y(), node2.give_z()

    # Priority queue
    q = []
    start_point = WirePoint(x_start, y_start, z_start)
    heapq.heappush(q, (0, start_point))

    # Keep track of g_cost (distance so far) and parents for path reconstruction
    costs = {start_point: 0}
    parents = {}

    # Already processed nodes
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
            grid.set_point_value(wire, 50) # The penalty for intersections tuned during experimental phase

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

            # Compute g_cost (distance so far)
            g_cost = costs[current] + grid.get_point_value(neighbor)
            f_cost = g_cost

            # If this new route to neighbor is cheaper, update
            if g_cost < costs.get(neighbor, float('inf')):
                costs[neighbor] = g_cost
                parents[neighbor] = current
                heapq.heappush(q, (f_cost, neighbor))

    # If the priority queue empties out and we never found a path:
    return None


def dfs_algorithm(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str) -> Wire|None:
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


def manhattan_wire(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str) -> Wire|None:
    """
    Creates a wire based on the Manhattan distance between node1 and node2.
    Ensures strictly Manhattan movement, with only one coordinate changing at a time.
    Avoids overlap with existing wires by dynamically rerouting and resolving conflicts.
    """
    wire = Wire(start_node=node1, end_node=node2, nodes_csv_path=nodes_csv_path, netlist_csv_path=netlist_csv_path)

    x1, y1 = node1.give_x(), node1.give_y()
    x2, y2 = node2.give_x(), node2.give_y()
    z = 0

    def move_one_step(current, target, fixed1, axis, z_level):
        """
        Move one step along the specified axis.
        `axis` can be 'x' or 'y', while `fixed1` and `fixed2` are the fixed coordinates.
        """
        step = 1 if current < target else -1
        next_point = WirePoint(current + step, fixed1, z_level) if axis == 'x' else WirePoint(fixed1, current + step, z_level)
        return next_point
    
    step_x = 1 if x1 < x2 else -1
    step_y = 1 if y1 < y2 else -1

    # Move along x-axis one step at a time
    while x1 != x2:
        next_point = move_one_step(x1, x2, y1, 'x', z)
        wire.add_wire_point(next_point)

        if z >= 7:
            break
        
        if not grid.check_valid_addition(wire):
            if y1 != y2:
                wire.pop_wire_point()
                next_point = move_one_step(y1, y2, x1, 'y', z)
                wire.add_wire_point(next_point)
            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                z += 1
                transition_point = WirePoint(x1, y1, z)
                wire.add_wire_point(transition_point)
                x1 = transition_point.give_x()
                y1 = transition_point.give_y()
                z = transition_point.give_z()
            else:
                x1 = next_point.give_x()
                y1 = next_point.give_y()
        else:
            x1 = next_point.give_x()

        if not grid.check_valid_addition(wire):
            grid.failed_wires += 1
        
    # Move along y-axis one step at a time
    while y1 != y2:
        next_point = move_one_step(y1, y2, x2, 'y', z)
        wire.add_wire_point(next_point)

        if z >= 7:
            break

        if not grid.check_valid_addition(wire):
            if x1 != x2:
                wire.pop_wire_point()
                next_point = move_one_step(x1, x2, y1, 'x', z)
                wire.add_wire_point(next_point)
            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                z += 1
                transition_point = WirePoint(x1, y1, z)
                wire.add_wire_point(transition_point)
                x2 = transition_point.give_x()
                y1 = transition_point.give_y()
                z = transition_point.give_z()
            else:
                x2 = next_point.give_x()
                y1 = next_point.give_y()
        else:
            y1 = next_point.give_y()

        if not grid.check_valid_addition(wire):
            grid.failed_wires += 1

    # Drop to z=0 after reaching the target x and y
    while z > 0:
        z -= 1
        descend_point = WirePoint(x2, y2, z)
        wire.add_wire_point(descend_point)

        if not grid.check_valid_addition(wire):
            wire.pop_wire_point()
            z += 1
            transition_point = WirePoint(x2 + step_x, y2, z)
            wire.add_wire_point(transition_point)
            transition_point = WirePoint(x2 + step_x, y2 + step_y, z)
            wire.add_wire_point(transition_point)
            transition_point = WirePoint(x2, y2 + step_y, z)
            wire.add_wire_point(transition_point)
            while z > 0:
                z -= 1
                transition_point = WirePoint(x2, y2 + step_y, z)
                wire.add_wire_point(transition_point)
            transition_point = WirePoint(x2, y2, z)
            wire.add_wire_point(transition_point)
        
        if not grid.check_valid_addition(wire):
            grid.failed_wires += 1

    # Ensure the final point (x2, y2, z=0) is added
    final_point = WirePoint(x2, y2, 0)
    if final_point not in wire.give_wirepoints():
        wire.add_wire_point(final_point)
        if not grid.check_obstacle(wire):
            raise ValueError(f"Failed to route wire from {node1} to {node2}.")

    grid.total_wires += 1
    
    # Add the completed wire to the grid
    grid.add_entire_wire_segments(wire)
    grid.add_wire_dict(wire)


    return wire
