import pandas as pd
import matplotlib.pyplot as plt
from nodes_class import Node, importeer_nodes
from wire_class import Wire, WirePoint, plot_wires_3d
from grid_class import Grid_3D
from code.import_netlist import importeer_netlist
import numpy as np

def maak_manhattan_wire(node1: Node, node2: Node, grid: Grid_3D):
    """
    Creëert een Wire op basis van Manhattan afstand tussen node1 en node2.
    Vermijdt overlap met bestaande wires door omhoog, omlaag of buiten de grid te bewegen.
    Nodes blijven altijd op de onderste laag (z=0).
    """
    wire = Wire(start_node=node1, end_node=node2)
    wire.wirepoints = []

    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y

    z = 0  # Startlaag
    current_point = WirePoint(x1, y1, z)  # Beginpunt
    wire.wirepoints.append(current_point)  # Voeg het startpunt toe

    def buitenom_punt(toevoegen_point, huidige_point):
        """
        Voeg een punt buiten de grid toe wanneer geen geldige route mogelijk is.
        """
        if toevoegen_point.x != huidige_point.x:  # Buitenom in de x-richting
            buiten_x = -1 if toevoegen_point.x < 0 else grid.n  # Links of rechts buiten de grid
            return WirePoint(buiten_x, huidige_point.y, huidige_point.z)
        elif toevoegen_point.y != huidige_point.y:  # Buitenom in de y-richting
            buiten_y = -1 if toevoegen_point.y < 0 else grid.m  # Boven of onder buiten de grid
            return WirePoint(huidige_point.x, buiten_y, huidige_point.z)
        else:
            return toevoegen_point  # Geen buitenom nodig

    # Beweeg horizontaal naar de eind-x
    if x1 != x2:
        step = 1 if x1 < x2 else -1
        for x in range(x1 + step, x2 + step, step):
            next_point = WirePoint(x, y1, z)

            if not grid.check_valid_addition(next_point, wire):
                z += 1  # Probeer omhoog te gaan
                transition_point = WirePoint(current_point.x, current_point.y, z)
                wire.wirepoints.append(transition_point)

                if not grid.check_valid_addition(next_point, wire):
                    buiten_punt = buitenom_punt(next_point, current_point)
                    wire.wirepoints.append(buiten_punt)
                    next_point = buiten_punt  # Werk verder vanaf het buitenom punt

            current_point = next_point
            wire.wirepoints.append(current_point)

    # Beweeg verticaal naar de eind-y
    if y1 != y2:
        step = 1 if y1 < y2 else -1
        for y in range(y1 + step, y2 + step, step):
            next_point = WirePoint(x2, y, z)

            if not grid.check_valid_addition(next_point, wire):
                z += 1  # Probeer omhoog te gaan
                transition_point = WirePoint(current_point.x, current_point.y, z)
                wire.wirepoints.append(transition_point)

                if not grid.check_valid_addition(next_point, wire):
                    buiten_punt = buitenom_punt(next_point, current_point)
                    wire.wirepoints.append(buiten_punt)
                    next_point = buiten_punt  # Werk verder vanaf het buitenom punt

            current_point = next_point
            wire.wirepoints.append(current_point)

    # Voeg het eindpunt toe (op z=0)
    if z > 0:
        # Voeg overgangspunt terug naar z=0 toe
        transition_point = WirePoint(current_point.x, current_point.y, z)
        wire.wirepoints.append(transition_point)

    final_point = WirePoint(x2, y2, 0)
    wire.wirepoints.append(final_point)

    # Update het grid en voeg de wire toe
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

            wire = maak_manhattan_wire(node1, node2, grid)

            # Voeg de wire toe aan de grid
            wires.append(wire)

        # Plot de wires in 3D
        plot_wires_3d(wires, breedte, lengte)

        # Bereken de kosten
        print(f"The total cost for this grid is: {grid.kosten()}")
    else:
        print("Er zijn niet genoeg nodes in de lijst om een wire te maken.")