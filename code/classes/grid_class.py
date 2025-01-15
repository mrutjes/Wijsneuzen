from code.classes.nodes_class import Node
from code.classes.wire_class import Wire
import matplotlib.pyplot as plt

class Grid_3D:
    def __init__(self, n, m):
        """
        Generates a grid of n x m x 8. 
        """
        self.n = n
        self.m = m
        self.height = 8
        self._wires = []
        self._nodes = []
        self._lines_count = 0
        self._point_dict = {
            (x, y, z): 0
            for x in range(self.n)
            for y in range(self.m)
            for z in range(self.height)
        }


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
        adds a wire to the wirepoint dictionary which is a property of the grid class.
        """
        from code.classes.wire_class import WirePoint
        for point in wire.give_wirepoints():
            x, y, z = point.give_x(), point.give_y(), point.give_z()
            if 0 <= x < self.n and 0 <= y < self.m and 0 <= z < self.height:
                self._point_dict[(x, y, z)] += 1
            else:
                raise IndexError("Coördinaten buiten de grid.")
        self._lines_count += len(wire.give_wirepoints()) - 1


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
        Checks if the wire does not run over another wire.
        """
        if len(self._wires) == 0:
            return True

        last_point = current_wire.give_wirepoints()[-3] #AANPASSEN
        point_to_add = current_wire.give_wirepoints()[-2] #AANPASSEN

        for wire in self._wires:
            for i in range(len(wire.give_wirepoints()) - 1):
                seg_start = wire.give_wirepoints()[i]
                seg_end = wire.give_wirepoints()[i + 1]

                for j in range(len(current_wire.give_wirepoints()) - 1):
                    current_start = current_wire.give_wirepoints()[j]
                    current_end = current_wire.give_wirepoints()[j + 1]

                    # Check voor kruisingen of overlappende segmenten
                    if (seg_start == current_end and seg_end == current_start) or \
                    (seg_start == current_start and seg_end == current_end):
                        return False
        return True

    def check_valid_addition(self, current_wire) -> bool:
        """
        Checks if the last point in the current wire wirepoints list does not overwrite any rules.
        """
        from code.classes.wire_class import WirePoint, Wire

        #Checks if the wirepoint is in the grid.
        wire_point = current_wire.give_wirepoints()[-2]
        if (wire_point.give_x(), wire_point.give_y(), wire_point.give_z()) not in self._point_dict:
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
