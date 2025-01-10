import pandas as pd
from nodes_class import importeer_nodes, Node

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
        self.aantal_lijnen = 0
        self.punt_dict = {
            (x, y, z): 0
            for x in range(self.n)
            for y in range(self.m)
            for z in range(self.hoogte)
        }

    def plaats_node(self, node: Node, z=0):
        if not (0 <= node.x < self.n and 0 <= node.y < self.m and 0 <= z < self.hoogte):
            raise IndexError("Coördinaten buiten de grid.")

    def wire_toevoegen_dict(self, wire):
        from wire_class import WirePoint
        for point in wire.wirepoints:
            x, y, z = point.x, point.y, point.z
            if 0 <= x < self.n and 0 <= y < self.m and 0 <= z < self.hoogte:
                self.punt_dict[(x, y, z)] += 1
            else:
                raise IndexError("Coördinaten buiten de grid.")
        self.aantal_lijnen += len(wire.wirepoints) - 1
        self.wires.append(wire)

    def nodes_uit_dictcount(self, nodes):
        for node in self.nodes:
            self.punt_dict[(node.x, node.y, 0)] = 0

    def afstand_tussen_nodes(self, node1: Node, node2: Node):
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    def check_valid_addition(self, point_to_add, current_wire):
        from wire_class import WirePoint

        if (wire.wirepoints[i+1] == point_to_add and wire.wirepoints[i] == current_wire.wirepoints[-2]):
            return False
        
        if not point_to_add in self.punt_dict:
            return False
        
        for wire in self.wires:
            for i in range(len(wire.wirepoints) - 1):
                if (wire.wirepoints[i+1] == point_to_add and wire.wirepoints[i] == current_wire.wirepoints[-2]):
                    return False
                
        if not current_wire.check_not_through_node(point_to_add):
            return False
        
        if not current_wire.check_not_return(point_to_add):
            return False
        return True
    
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
