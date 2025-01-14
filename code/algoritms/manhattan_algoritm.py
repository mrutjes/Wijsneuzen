import pandas as pd
import matplotlib.pyplot as plt
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
import numpy as np

def manhattan_wire(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str):
    """
    Creates a wire based on the Manhattan distance between node1 and node2.
    Ensures strictly Manhattan movement, with only one coordinate changing at a time.
    Avoids overlap with existing wires by dynamically rerouting and resolving conflicts.
    """
    wire = Wire(start_node=node1, end_node=node2, nodes_csv_path=nodes_csv_path)

    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y
    z = 0  # Start on the bottom layer
    visited = set()

    def is_visited(point):
        """Check if a point has already been visited."""
        return (point.x, point.y, point.z) in visited

    def mark_visited(point):
        """Mark a point as visited."""
        visited.add((point.x, point.y, point.z))

    def move_one_step(current, target, fixed1, fixed2, axis, z_level):
        """
        Move one step along the specified axis.
        `axis` can be 'x' or 'y', while `fixed1` and `fixed2` are the fixed coordinates.
        """
        step = 1 if current < target else -1
        next_point = WirePoint(current + step, fixed1, z_level) if axis == 'x' else WirePoint(fixed1, current + step, z_level)
        return next_point

    # Move along x-axis one step at a time
    while x1 != x2:
        next_point = move_one_step(x1, x2, y1, z, 'x', z)
        if is_visited(next_point):
            continue
        wire.add_wire_point(next_point)
        mark_visited(next_point)

        if not grid.check_valid_addition(wire):
            # Handle conflict by moving up one layer
            wire.pop_wire_point()
            z += 1
            transition_point = WirePoint(x1, y1, z)
            wire.add_wire_point(transition_point)
            mark_visited(transition_point)
        else:
            x1 = next_point.x

    # Move along y-axis one step at a time
    while y1 != y2:
        next_point = move_one_step(y1, y2, x1, z, 'y', z)
        if is_visited(next_point):
            continue
        wire.add_wire_point(next_point)
        mark_visited(next_point)

        if not grid.check_valid_addition(wire):
            # Handle conflict by moving up one layer
            wire.pop_wire_point()
            z += 1
            transition_point = WirePoint(x1, y1, z)
            wire.add_wire_point(transition_point)
            mark_visited(transition_point)
        else:
            y1 = next_point.y

    # Drop to z=0 after reaching the target x and y
    while z > 0:
        z -= 1
        descent_point = WirePoint(x2, y2, z)
        if is_visited(descent_point):
            continue
        wire.add_wire_point(descent_point)
        mark_visited(descent_point)

        if not grid.check_valid_addition(wire):
            wire.pop_wire_point()
            continue

    # Ensure the final point (x2, y2, z=0) is added
    final_point = WirePoint(x2, y2, 0)
    if final_point not in wire.wirepoints:
        wire.add_wire_point(final_point)
        mark_visited(final_point)
        if not grid.check_valid_addition(wire):
            raise ValueError(f"Failed to route wire from {node1} to {node2}.")

    # Add the completed wire to the grid
    grid.add_wire_dict(wire)
    return wire
