import pandas as pd
import matplotlib.pyplot as plt
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
import numpy as np

def manhattan_wire(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str):
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

        # HEEL OMSLACHTIG GEDAAN ZODAT IK HET STAP VOOR STAP KON OPZETTEN MAAR MOET LATER GEWOON EVEN NETJES MET LOOPS
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
    print(f'Segment set: {wire.give_segments()}')
    grid.add_entire_wire_segments(wire)
    grid.add_wire_dict(wire)
    return wire
