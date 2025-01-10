import pandas as pd
import matplotlib.pyplot as plt
from nodes_class import Node, importeer_nodes
from wire_class import Wire, WirePoint
from grid_class import Grid_3D
from connections_class import importeer_netlist
import numpy as np


# Functie om een wire aan te maken op basis van Manhattan-afstand
def maak_manhattan_wire(node1: Node, node2: Node):
    """Creëert een Wire op basis van Manhattan afstand tussen node1 en node2."""
    wirepoints = []
    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y

    # Beweeg horizontaal naar de eind-x
    if x1 != x2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            point = WirePoint(x, y1, 0)
            if point not in wirepoints and point != WirePoint(x2, y2, 0):  # Vermijd duplicaten en eindnode
                wirepoints.append(point)

    # Beweeg verticaal naar de eind-y
    if y1 != y2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            point = WirePoint(x2, y, 0)
            if point not in wirepoints and point != WirePoint(x1, y1, 0):  # Vermijd duplicaten en startnode
                wirepoints.append(point)

    # Voeg de eindnode alleen toe als deze uniek is en niet direct verbonden is
    if WirePoint(x2, y2, 0) not in wirepoints:
        wirepoints.append(WirePoint(x2, y2, 0))

    # Maak de wire aan met de lijst van wirepoints en de start- en eindnodes
    return Wire(start_node=node1, end_node=node2, wirepoints=wirepoints)


def plot_wires_3d(wires, breedte, lengte):
    """
    Plot alle wires in een 3D-figuur, waarbij de lijnsegmenten langs de wirepoints lopen (manhattan-afstand).
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for wire in wires:
        xs = [p.x for p in wire.wirepoints]
        ys = [p.y for p in wire.wirepoints]
        zs = [p.z for p in wire.wirepoints]
        
        # Teken de lijnen langs de wirepoints
        ax.plot(xs, ys, zs, marker='o')

    ax.set_xlim(0, breedte)
    ax.set_ylim(0, lengte)
    ax.set_zlim(0, 7)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

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
    print(netlist)

    # Maak een wire tussen de nodes in de netlist
    if len(netlist) >= 1:
        # Maak meerdere wires tussen verschillende nodes
        wires = []
        for i in range(0, len(netlist)):
            node1 = netlist[i][0]
            node2 = netlist[i][1]

            node1 = nodes_list[node1 - 1]
            node2 = nodes_list[node2 - 1]
            wire = maak_manhattan_wire(node1, node2)

            # Voeg de wire toe aan het grid
            wires.append(wire)

        # Plot de wires in 3D
        plot_wires_3d(wires, breedte, lengte)

        # Bereken de kosten
        print(f"The total cost for this grid is: {grid.kosten()}")
    else:
        print("Er zijn niet genoeg nodes in de lijst om een wire te maken.")
