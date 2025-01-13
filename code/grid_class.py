import pandas as pd
from nodes_class import import_nodes, Node


class Grid_3D:
    def __init__(self, n, m):
        """
        Generates a grid of n x m x 8. 
        """
        self.n = n
        self.m = m
        self.height = 8
        self.wires = []
        self.nodes = []
        self.lines_count = 0
        self.point_dict = {
            (x, y, z): 0
            for x in range(self.n)
            for y in range(self.m)
            for z in range(self.height)
        }


    def place_node(self, node: Node, z=0) -> None:
        """
        Places a node at the baselayer level at given coordinates.
        """
        if not (0 <= node.x < self.n and 0 <= node.y < self.m and 0 <= z < self.height):
            raise IndexError("Coördinaten buiten de grid.")


    def add_wire_dict(self, wire) -> None:
        """
        adds a wire to the wirepoint dictionary which is a property of the grid class.
        """
        from wire_class import WirePoint
        for point in wire.wirepoints:
            x, y, z = point.x, point.y, point.z
            if 0 <= x < self.n and 0 <= y < self.m and 0 <= z < self.height:
                self.point_dict[(x, y, z)] += 1
            else:
                raise IndexError("Coördinaten buiten de grid.")
        self.lines_count += len(wire.wirepoints) - 1
        self.wires.append(wire)


    def remove_nodes_pointdict(self):
        """
        Removes the nodes from the point dictionary, to make sure they don't count as intersections
        """
        for node in self.nodes:
            self.point_dict[(node.x, node.y, 0)] = 0


    def distance_nodes(self, node1: Node, node2: Node) -> int:
        """
        Returns the manhattan distance between two nodes.
        """
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)
    
    
    def check_wire_overlap(self, current_wire) -> bool:
        """
        Checks if the wire does not run over another wire.
        """
        if len(self.wires) == 0:
            return True

        last_point = current_wire.wirepoints[-3]
        point_to_add = current_wire.wirepoints[-2]

        for wire in self.wires:
            for i in range(len(wire.wirepoints) - 1):
                if (wire.wirepoints[i] == point_to_add and
                    wire.wirepoints[i + 1] == last_point) or (wire.wirepoints[i +1] == point_to_add and
                    wire.wirepoints[i] == last_point):

                    return False


    def check_valid_addition(self, current_wire) -> bool:
        """
        Checks if the last point in the current wire wirepoints list does not overwrite any rules.
        """
        from wire_class import WirePoint, Wire

        #Checks if the wirepoint is in the grid.
        wire_point = current_wire.wirepoints[-2]
        if (wire_point.x, wire_point.y, wire_point.z) not in self.point_dict:
            return False

        #Checks if the wirepoint does not run over another wire.
        if not self.check_wire_overlap(current_wire):
            return False
                
        #Checks if the wirepoint does not go through node.
        if not current_wire.check_not_through_node():
            return False
        
        #Checks if the wire does not return on itself
        if not current_wire.check_not_return():
            return False

        return True


    def total_intersections(self) -> int:
        """
        Calculates the total intersections based on if the value of the point dict is larger than 1.
        """
        intersections = 0
        for value in self.point_dict.values():
            if value > 1:
                intersections += (value - 1)
        return intersections


    def cost(self) -> int:
        """
        Calculates the total cost:
        - 300 per intersection
        - 1 per line
        """
        intersections = self.total_intersections()
        return intersections * 300 + self.lines_count
