from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
import matplotlib.pyplot as plt
from code.imports import import_netlist, import_nodes
from code.classes.segment_class import Segment

class Grid_3D:
    def __init__(self, n, m, nodes_csv_path):
        """
        Generates a grid of n x m x 8. 
        """
        self.n = n
        self.m = m
        self.height = 8
        self._wires = []
        self._lines_count = 0
        self._segments = set()
        self._nodes = import_nodes(nodes_csv_path)
        self._reserved_points = set()
        self._point_dict = {
            (x, y, z): 0
            for x in range(self.n)
            for y in range(self.m)
            for z in range(self.height)
        }


    def give_height(self) -> int:
        """
        Returns the height of the grid.
        """
        return self.n
    

    def give_width(self) -> int:
        """
        Returns the width of the grid.
        """
        return self.m


    def place_node(self, node: Node, z=0) -> None:
        """
        Places a node at the baselayer level at given coordinates.
        """
        if not (0 <= node.give_x() < self.n and 0 <= node.give_y() < self.m and 0 <= z < self.height):
            raise IndexError("Coördinaten buiten de grid.")
        
    
    def add_wire_list(self, wire) -> None:
        """
        Add a wire to the list of wires
        """
        self._wires.append(wire)


    def return_wire_list(self) -> list[Wire]:
        """
        Returns the list of wires
        """
        return self._wires


    def add_wire_dict(self, wire) -> None:
        """
        Adds a wire to the wirepoint dictionary and updates the segment set.
        """
        from code.classes.wire_class import WirePoint

        wirepoints = wire.give_wirepoints()
        for i in range(len(wirepoints) - 1):
            start_point = wirepoints[i]
            end_point = wirepoints[i + 1]

            # Add segment to the set
            segment = Segment(start_point, end_point)
            self._segments.add(segment)

            x, y, z = start_point.give_x(), start_point.give_y(), start_point.give_z()
            if 0 <= x < self.n and 0 <= y < self.m and 0 <= z < self.height:
                self._point_dict[(x, y, z)] += 1
            else:
                raise IndexError("Coordinates outside the grid.")
        
        self._lines_count += len(wirepoints) - 1


    def remove_nodes_pointdict(self):
        """
        Removes the nodes from the point dictionary, to make sure they don't count as intersections
        """
        for node in self._nodes:
            self._point_dict[(node.give_x(), node.give_y(), 0)] = 0


    def distance_nodes(self, node1: Node, node2: Node) -> int:
        """
        Returns the manhattan distance between two nodes.
        """
        return abs(node1.give_x() - node2.give_x()) + abs(node1.give_y() - node2.give_y())
    
    
    def check_wire_overlap(self, current_wire) -> bool:
        """
        Checks if the wire does not run over another wire in any direction.
        Uses the precomputed set of segments for efficient checks.
        """
        if len(self._segments) == 0:
            return True

        # Create segments for the current wire
        current_segments = [
            Segment(current_wire.give_wirepoints()[i], current_wire.give_wirepoints()[i + 1])
            for i in range(len(current_wire.give_wirepoints()) - 1)
        ]   

        # Check for overlap with any existing segments
        for current_segment in current_segments:
            if current_segment in self._segments:
                print(f"Overlap detected with segment: {current_segment}")
                return False

        return True
    
    def add_reservation(self, point: WirePoint) -> None:
        """
        Adds the given point to reserved points, as well as the neighboring points
        (x-1, x+1, y-1, y+1, and z+1).
        """

        # Extract coordinates
        x, y, z = point.give_x(), point.give_y(), point.give_z()

        # Add the neighboring points
        self._reserved_points.add(WirePoint(x - 1, y, z))
        self._reserved_points.add(WirePoint(x + 1, y, z))
        self._reserved_points.add(WirePoint(x, y - 1, z))
        self._reserved_points.add(WirePoint(x, y + 1, z))
        self._reserved_points.add(WirePoint(x, y, z + 1))
    

    def check_reservation(self, point: WirePoint) -> bool:
        """
        Checks if a wire does not go over a reserved point
        """
        if (WirePoint(point.give_x(), point.give_y(), point.give_z())) in self._reserved_points:
            return False
        
        return True


    def check_valid_addition(self, current_wire: Wire) -> bool:
        """
        Checks if the last point in the current wire wirepoints list does not overwrite any rules.
        """
        from code.classes.wire_class import WirePoint, Wire

            # Ensure the wire has at least two points
        if len(current_wire.give_wirepoints()) < 2:
            return False

        #Checks if the wirepoint is in the grid.
        wire_point = current_wire.give_wirepoints()[-2]
        if (wire_point.give_x(), wire_point.give_y(), wire_point.give_z()) not in self._point_dict:
            return False

        #Checks if the wirepoint does not run over another wire.
        if not self.check_wire_overlap(current_wire):
            print("Would run over another wire")
            return False
                
        #Checks if the wirepoint does not go through node.
        if not current_wire.check_not_through_node():
            print("Would run through node")
            return False
        
        #Checks if the wire does not return on itself
        if not current_wire.check_not_return():
            print("Would return on itself")
            return False
        
        #if not self.check_reservation(wire_point):
        #    return False

        return True


    def total_intersections(self) -> int:
        """
        Calculates the total intersections based on if the value of the point dict is larger than 1.
        """
        intersections = 0
        for value in self._point_dict.values():
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
        return intersections * 300 + self._lines_count

   
def plot_wires_3d(wires: list[Wire], grid_width: int, grid_height: int):
    """
    A function used to plot the wires of the grid in 3D.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for wire in wires:
        xs = [p.give_x() for p in wire.give_wirepoints()]
        ys = [p.give_y() for p in wire.give_wirepoints()]
        zs = [p.give_z() for p in wire.give_wirepoints()]
        
        # Teken de lijnen langs de wirepoints
        ax.plot(xs, ys, zs, marker='o')

    ax.set_xlim(0, grid_width)
    ax.set_ylim(0, grid_height)
    ax.set_zlim(0, 7)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
