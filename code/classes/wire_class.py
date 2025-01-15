from code.classes.nodes_class import Node
from code.imports import import_nodes

class WirePoint:
    """
    A wire exists of Wirepoints, these have the attributes of x y and z coordinates
    """
    def __init__(self, x, y, z) -> None:
        self._x = x
        self._y = y
        self._z = z


    def __eq__(self, other):
        if not isinstance(other, WirePoint):
            return False
        return (self._x, self._y, self._z) == (other._x, other._y, other._z)
    

    def __hash__(self):
        return hash((self._x, self._y, self._z))
        

    def give_place(self) -> (int,int,int): # type: ignore
        """
        Returns the coordinates of a wirepoint as integers.
        """
        return (self._x, self._y, self._z)
    

    def give_x(self) -> int:
        """
        Returns the x coordinate of a wirepoint.
        """
        return self._x
    

    def give_y(self) -> int:
        """
        Returns the y coordinate of a wirepoint.
        """
        return self._y
    
    
    def give_z(self) -> int:
        """
        Returns the z coordinate of a wirepoint.
        """
        return self._z
        

class Wire:
    """
    A class to combine wirepoints in order to form a wire.
    """

    def __init__(self, start_node: Node, end_node: Node, nodes_csv_path: str) -> None:
        self.start_node = start_node
        self.end_node = end_node
        self._wirepoints = [WirePoint(self.start_node.give_x(), self.start_node.give_y(), 0), WirePoint(self.end_node.give_x(), self.end_node.give_y(), 0)]
        self._nodes = import_nodes(nodes_csv_path)


    def add_wire_point(self, wire_point: WirePoint) -> None:
        """
        Adds a given wirepoint to the wire. The wirepoints list is always consistent of the start and end node.
        """
        self._wirepoints.remove(self._wirepoints[-1])
        self._wirepoints.append(wire_point)
        self._wirepoints.append(WirePoint(self.end_node.give_x(), self.end_node.give_y(), 0))


    def give_wirepoints(self) -> list[WirePoint]:
        """
        Returns the wirepoints of the wire.
        """
        return self._wirepoints
    

    def check_wire(self) -> bool:
        """
        Checks if a wire is uninterrupted.
        """
        for i in range(len(self._wirepoints) - 1):
            current = self._wirepoints[i]
            next_point = self._wirepoints[i + 1]
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
        first_wp = self._wirepoints[0]
        last_wp = self._wirepoints[-1]
        return (
            ((first_wp.give_x(), first_wp.give_y()) == (self.start_node.give_x(), self.start_node.give_y()) and
             (last_wp.give_x(), last_wp.give_y()) == (self.end_node.give_x(), self.end_node.give_y()))
            or
            ((first_wp.give_x(), first_wp.give_y()) == (self.end_node.give_x(), self.end_node.give_y()) and
             (last_wp.give_x(), last_wp.give_y()) == (self.start_node.give_x(), self.start_node.give_y()))
        )
    

    def check_not_through_node(self) -> bool:
        """
        Checks if a wire does not run through a node.
        """
        if self._wirepoints[-2].give_z() != 0:
            return True
        
        for node in self._nodes:
            if (((self._wirepoints[-2].give_x(),self._wirepoints[-2].give_y()) == (node.give_x(),node.give_y())) and 
                ((self._wirepoints[-2].give_x(),self._wirepoints[-2].give_y()) != (self.end_node.give_x(), self.end_node.give_y())) and
                ((self._wirepoints[-2].give_x(),self._wirepoints[-2].give_y()) != (self.start_node.give_x(), self.start_node.give_y()))):
                return False
        
        return True
    

    def check_not_return(self) -> bool:
        """
        Check if the wire does not return on itself.
        """

        # If there are fewer than 4 points, a return is impossible.
        if len(self._wirepoints) < 4:
            return True

        # The last two points form the most recently added segment.
        last_point = self._wirepoints[-2]
        point_to_add = self._wirepoints[-1]

        # Check if the new segment reverses any previous segment.
        for i in range(len(self._wirepoints) - 2):
            seg_start = self._wirepoints[i]
            seg_end = self._wirepoints[i + 1]

            # If the new segment (point_to_add -> last_point) is the reverse of an existing segment, return False.
            if seg_start == point_to_add and seg_end == last_point:
                return False

        return True

    def pop_wire_point(self) -> None:
        """
        Pops the last item in the wirepoints list (except the end node).
        """
        self._wirepoints.pop(-2)




