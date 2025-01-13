from nodes_class import Node, import_nodes
import matplotlib.pyplot as plt

class WirePoint:
    """
    A wire exists of Wirepoints, these have the attributes of x y and z coordinates
    """
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z


    def __eq__(self, other):
        if not isinstance(other, WirePoint):
            return False
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    

    def __hash__(self):
        return hash((self.x, self.y, self.z))
        

    def give_place(self) -> (int,int,int): # type: ignore
        """
        Returns the coordinates of a wirepoint as integers.
        """
        return (self.x, self.y, self.z)
    

    def give_x(self) -> int:
        """
        Returns the x coordinate of a wirepoint.
        """
        return self.x
    

    def give_y(self) -> int:
        """
        Returns the y coordinate of a wirepoint.
        """
        return self.y
    
    
    def give_z(self) -> int:
        """
        Returns the z coordinate of a wirepoint.
        """
        return self.z
        

class Wire:
    """
    A class to combine wirepoints in order to form a wire.
    """

    def __init__(self, start_node: Node, end_node: Node) -> None:
        self.start_node = start_node
        self.end_node = end_node
        self.wirepoints = [WirePoint(self.start_node.x, self.start_node.y, 0), WirePoint(self.end_node.x, self.end_node.y, 0)]
        self.nodes = import_nodes('../gates&netlists/chip_0/print_0.csv')
    

    def __eq__(self, other):
        if not isinstance(other, WirePoint):
            return False
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)


    def __repr__(self):
        return f"WirePoint({self.x}, {self.y}, {self.z})"


    def add_wire_point(self, wire_point: WirePoint) -> None:
        """
        Adds a given wirepoint to the wire. The wirepoints list is always consistent of the start and end node.
        """
        self.wirepoints.remove(self.wirepoints[-1])
        self.wirepoints.append(wire_point)
        self.wirepoints.append(WirePoint(self.end_node.x, self.end_node.y, 0))


    def check_wire(self) -> bool:
        """
        Checks if a wire is uninterrupted.
        """
        for i in range(len(self.wirepoints) - 1):
            current = self.wirepoints[i]
            next_point = self.wirepoints[i + 1]
            if not (
                (abs(current.give_x() - next_point.give_x()) == 1 and
                 current.give_y() == next_point.give_y() and
                 current.give_z() == next_point.give_z()) or
                (abs(current.give_y() - next_point.give_y()) == 1 and
                 current.give_x() == next_point.give_x() and
                 current.give_z() == next_point.give_z()) or
                (abs(current.give_z() - next_point.give_z()) == 1 and
                 current.give_x() == next_point.give_x() and
                 current.give_y() == next_point.give_y())
            ):
                return False
            
        return True


    def check_connection(self) -> bool:
        """
        Checks if a wire connects two nodes that are valid in the netlist.
        """
        first_wp = self.wirepoints[0]
        last_wp = self.wirepoints[-1]
        return (
            ((first_wp.x, first_wp.y) == (self.start_node.x, self.start_node.y) and
             (last_wp.x, last_wp.y) == (self.end_node.x, self.end_node.y))
            or
            ((first_wp.x, first_wp.y) == (self.end_node.x, self.end_node.y) and
             (last_wp.x, last_wp.y) == (self.start_node.x, self.start_node.y))
        )
    

    def check_not_through_node(self) -> bool:
        """
        Checks if a wire does not run through a node.
        """
        if self.wirepoints[-2].z != 0:
            return True
        
        for node in self.nodes:
            if ((self.wirepoints[-2].x,self.wirepoints[-2].y) == (node.x,node.y) and 
                ((self.wirepoints[-2].x,self.wirepoints[-2].y) != (self.end_node.x, self.end_node.y)) and
                ((self.wirepoints[-2].x,self.wirepoints[-2].y) != (self.start_node.x, self.start_node.y))):
                return False
        
        return True
    

    def check_not_return(self) -> bool:
        """
        Check if the wire does not return on itself.
        """

        # If there are fewer than 4 points, a return is impossible.
        if len(self.wirepoints) < 4:
            return True

        # The last two points form the most recently added segment.
        last_point = self.wirepoints[-2]
        point_to_add = self.wirepoints[-1]

        # Check if the new segment reverses any previous segment.
        for i in range(len(self.wirepoints) - 2):
            seg_start = self.wirepoints[i]
            seg_end = self.wirepoints[i + 1]

            # If the new segment (point_to_add -> last_point) is the reverse of an existing segment, return False.
            if seg_start == point_to_add and seg_end == last_point:
                return False

        return True

    def pop_wire_point(self) -> None:
        """
        Pops the last item in the wirepoints list (except the end node).
        """
        self.wirepoints.pop(-2)


def plot_wires_3d(wires, breedte, lengte):
    """
    A function used to plot the wires of the grid in 3D.
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

