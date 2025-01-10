import pandas as pd
from nodes_class import Node, importeer_nodes

class Grid_3D:
    def __init__(self, n, m):
        """
        Maakt een grid van n x m x 8.
        n = x-dimensie, m = y-dimensie, 'hoogte' = 8.
        """
        self.n = n
        self.m = m
        self.hoogte = 8
        self.wires = []
        self.nodes = importeer_nodes('../gates&netlists/chip_0/print_0.csv')
        # aantal_lijnen houdt bij hoeveel stukjes wire in totaal geplaatst zijn
        self.aantal_lijnen = 0

        # punt_dict houdt bij hoe vaak elk grid-punt (x,y,z) wordt doorkruist
        self.punt_dict = {
            (x, y, z): 0
            for x in range(self.n)
            for y in range(self.m)
            for z in range(self.hoogte)
        }

    def tel_lijnen_punt(self):
        """Retourneert de dictionary met het aantal lijnen per (x,y,z)."""
        return self.punt_dict

    def totaal_kruisingen(self):
        """
        Berekent het totale aantal 'kruisingen':
        elke plek in punt_dict met waarde > 1 is een kruising.
        """
        kruisingen = 0
        for waarde in self.punt_dict.values():
            if waarde > 1:
                kruisingen += (waarde - 1)
        return kruisingen

    def kosten(self):
        """
        Berekent de kosten:
        - Kruisingen: elke kruising kost 300.
        - Aantal lijnen: elke lijn kost 1.
        """
        kruisingen = self.totaal_kruisingen()
        return kruisingen * 300 + self.aantal_lijnen
    
    def plaats_node(self, node: Node, z=0):
        """
        Plaatst een node op (node.x, node.y, z).
        In deze code doen we verder niets met die plaatsing,
        maar je kunt hier bijvoorbeeld in een eigen datastructuur opslaan waar je nodes zitten.
        """
        if not (0 <= node.x < self.n and 0 <= node.y < self.m and 0 <= z < self.hoogte):
            raise IndexError("Coördinaten buiten de grid.")

    def wire_toevoegen_dict(self, wire):
        """
        Verhoogt in punt_dict de teller voor elk WirePoint in wire
        en past aantal_lijnen aan.
        """
        # doorloop alle wirepoints
        for point in wire.wirepoints:
            x, y, z = point.x, point.y, point.z
            if 0 <= x < self.n and 0 <= y < self.m and 0 <= z < self.hoogte:
                self.punt_dict[(x, y, z)] += 1
            else:
                raise IndexError("Coördinaten buiten de grid.")
        # elke 'wire' met N wirepoints telt (N-1) lijnstukjes
        self.aantal_lijnen += len(wire.wirepoints) - 1

        self.wires.append(wire)

    def nodes_uit_dictcount(self, nodes):
        """zet de waarden van de nodes coordinaten op nul in de dict."""
        for node in self.nodes:
            self.punt_dict[(node.x, node.y, 0)] = 0

    def afstand_tussen_nodes(self, node1: Node, node2: Node):
        """Berekent de Manhattan-afstand tussen twee nodes."""
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)