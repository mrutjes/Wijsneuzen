import pandas as pd
import matplotlib.pyplot as plt
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
import numpy as np


def manhattan_wire(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str):
    """
    Creëert een Wire op basis van Manhattan afstand tussen node1 en node2.
    Vermijdt overlap met bestaande wires door omhoog, omlaag of buiten de grid te bewegen.
    Nodes blijven altijd op de onderste laag (z=0).
    """
    wire = Wire(start_node=node1, end_node=node2, nodes_csv_path=nodes_csv_path)

    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y

    z = 0
    # Beweeg horizontaal naar de eind-x
    if x1 != x2:
        step = 1 if x1 < x2 else -1
        for x in range(x1 + 1, x2 + step, step):
            point = WirePoint(x, y1, z)
            if point != WirePoint(x2, y2, 0):
                wire.add_wire_point(point)

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                z += 1
                transition_point = WirePoint(x -1, y1, z)
                wire.add_wire_point(transition_point)

    # Beweeg verticaal naar de eind-y
    if y1 != y2:
        step = 1 if y1 < y2 else -1
        for y in range(y1 + 1, y2 + step, step):
            point = WirePoint(x2, y, z)
            if point != WirePoint(x2, y2, 0):
                wire.add_wire_point(point)

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                z += 1
                transition_point = WirePoint(x2, y -1, z)
                wire.add_wire_point(transition_point)

    # Drop down to z=0
    while z > 0:
        z -= 1
        next_point = WirePoint(x2, y2, z)
        wire.add_wire_point(next_point)

        # Check if there is no overlapping wire in its place
        if not grid.check_valid_addition(wire):
            wire.pop_wire_point()
            continue

    # Add wire to dict
    grid.add_wire_dict(wire)
    return wire