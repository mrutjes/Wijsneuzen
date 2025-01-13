import pandas as pd
import matplotlib.pyplot as plt
from nodes_class import Node, importeer_nodes
from wire_class import Wire, WirePoint, plot_wires_3d
from grid_class import Grid_3D
from connections_class import importeer_netlist
import numpy as np

def maak_manhattan_wire(node1: Node, node2: Node, grid: Grid_3D):
    """
    Creëert een Wire op basis van Manhattan afstand tussen node1 en node2.
    Vermijdt overlap met bestaande wires door omhoog, omlaag of buiten de grid te bewegen.
    Nodes blijven altijd op de onderste laag (z=0).
    """
    wire = Wire(start_node=node1, end_node=node2)

    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y

    z = 0
    # Beweeg horizontaal naar de eind-x
    if x1 != x2:
        step = 1 if x1 < x2 else -1
        for x in range(x1, x2 + step, step):
            point = WirePoint(x, y1, z)
            if point != WirePoint(x2, y2, 0):
                wire.add_wire_point(point)

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                z += 1
                transition_point = WirePoint(x, y1, z)
                wire.add_wire_point(transition_point)

    # Beweeg verticaal naar de eind-y
    if y1 != y2:
        step = 1 if y1 < y2 else -1
        for y in range(y1, y2 + step, step):
            point = WirePoint(x2, y, z)
            if point != WirePoint(x2, y2, 0):
                wire.add_wire_point(point)

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                z += 1
                transition_point = WirePoint(x2, y, z)
                wire.add_wire_point(transition_point)

    # Veilig afdalen naar z = 0
    while z > 0:
        z -= 1
        next_point = WirePoint(x2, y2, z)
        wire.add_wire_point(next_point)

        # Check als afdaling niet mogelijk is
        if not grid.check_valid_addition(wire):
            wire.pop_wire_point()  # Blijf op huidige laag
            continue  # Probeer opnieuw met een lagere z

    # Voeg de wire toe aan de grid
    grid.wire_toevoegen_dict(wire)
    return wire

# Hoofdcode om alles te gebruiken
if __name__ == '__main__':
    # Initieer het grid
    breedte = 10
    lengte = 10
    grid = Grid_3D(breedte, lengte)  # Grid van 10x10

    # Nodes importeren en toevoegen vanuit het opgegeven CSV-bestand
    nodes_list = importeer_nodes('../gates&netlists/chip_0/print_0.csv')
    for node in nodes_list:
        grid.plaats_node(node)

    # Netlist importeren
    netlist = importeer_netlist('../gates&netlists/chip_0/netlist_1.csv')

    # Maak een wire tussen de nodes in de netlist
    if len(netlist) >= 1:
        # Maak meerdere wires tussen verschillende nodes
        wires = []
        for i in range(0, len(netlist)):
            node1 = netlist[i][0]
            node2 = netlist[i][1]

            node1 = nodes_list[node1 - 1]
            node2 = nodes_list[node2 - 1]

            wire = maak_manhattan_wire(node1, node2, grid)

            # Voeg de wire toe aan de grid
            wires.append(wire)

        # Plot de wires in 3D
        plot_wires_3d(wires, breedte, lengte)

        # Bereken de kosten
        print(f"The total cost for this grid is: {grid.kosten()}")
    else:
        print("Er zijn niet genoeg nodes in de lijst om een wire te maken.")