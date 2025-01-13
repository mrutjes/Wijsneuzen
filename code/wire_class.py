from nodes_class import Node, importeer_nodes
import matplotlib.pyplot as plt

class WirePoint:
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
        
    def give_place(self):
        return (self.x, self.y, self.z)
    
    def give_x(self) -> int:
        return self.x
    
    def give_y(self) -> int:
        return self.y
    
    def give_z(self) -> int:
        return self.z
        
class Wire:
    def __init__(self, start_node: Node, end_node: Node) -> None:
        self.start_node = start_node
        self.end_node = end_node
        self.wirepoints = [WirePoint(self.start_node.x, self.start_node.y, 0), WirePoint(self.end_node.x, self.end_node.y, 0)]
        self.nodes = importeer_nodes('../gates&netlists/chip_0/print_0.csv')
    
    def __eq__(self, other):
        if not isinstance(other, WirePoint):
            return False
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __repr__(self):
        return f"WirePoint({self.x}, {self.y}, {self.z})"

    def add_wire_point(self, wire_point: WirePoint) -> None:
        self.wirepoints.remove(self.wirepoints[-1])
        self.wirepoints.append(wire_point)
        self.wirepoints.append(WirePoint(self.end_node.x, self.end_node.y, 0))

    def check_wire(self) -> bool:
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
        if self.wirepoints[-2].z != 0:
            return True
        
        for node in self.nodes:
            if ((self.wirepoints[-2].x,self.wirepoints[-2].y) == (node.x,node.y)):
                return False
        
        return True
    
    def check_not_return(self) -> bool:
        """Check if the wire does not return on itself."""

        if len(self.wirepoints) < 4:
            return True
        
        last_point = self.wirepoints[-3]
        point_to_add = self.wirepoints[-2]

        for i in range(len(self.wirepoints) - 2):
            seg_start = self.wirepoints[i]
            seg_end = self.wirepoints[i + 1]
            if seg_start == point_to_add and seg_end == last_point:
                return False

        return True

    def pop_wire_point(self) -> None:
        self.wirepoints.pop(-2)


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

