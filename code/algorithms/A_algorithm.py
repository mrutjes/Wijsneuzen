import heapq
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D

def heuristic(point: WirePoint, goal: WirePoint) -> int:
    """
    Calculate the Manhattan distance from the current point to the goal.
    """
    return (
        abs(point.give_x() - goal.give_x()) +
        abs(point.give_y() - goal.give_y()) +
        abs(point.give_z() - goal.give_z())
    )

def reconstruct_path(came_from, start, end):
    """
    Reconstruct the path from the start to the end using the came_from dictionary.
    """
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def a_star(grid: Grid_3D, node1: Node, node2: Node, nodes_csv_path: str, netlist_csv_path: str):
    """
    Implements the A* algorithm for routing wires between two nodes in a 3D grid.
    """
    start = WirePoint(node1.give_x(), node1.give_y(), 0)
    end = WirePoint(node2.give_x(), node2.give_y(), 0)

    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == end:
            return reconstruct_path(came_from, start, end)

        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            neighbor = WirePoint(current.give_x() + dx, current.give_y() + dy, current.give_z() + dz)

            if not grid.check_in_grid(neighbor):
                continue

            if not grid.check_not_through_node(neighbor):
                continue

            new_cost = cost_so_far[current] + 1  # Cost to move to the neighbor

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(open_list, (priority, neighbor))
                came_from[neighbor] = current

    return None  # No path found

def route_netlist(grid: Grid_3D, netlist: list[tuple[Node, Node]]):
    """
    Routes all nets in the given netlist on the grid using the A* algorithm.
    """
    for net in netlist:
        start_node, end_node = net

        path = a_star(grid, start_node, end_node, grid.nodes_csv_path, None)

        if path:
            wire = Wire(start_node=start_node, end_node=end_node, nodes_csv_path=grid.nodes_csv_path, netlist_csv_path=None)
            for point in path:
                wire.add_wire_point(point)

            if grid.check_valid_addition(wire):
                grid.add_wire_dict(wire)
                grid.total_wires += 1
            else:
                raise Exception(f"Failed to route net from {start_node} to {end_node}")
        else:
            raise Exception(f"Net could not be routed between {start_node} and {end_node}")

    return grid
