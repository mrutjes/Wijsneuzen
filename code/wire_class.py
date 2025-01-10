from nodes_class import Node

class WirePoint:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

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
        self.nodes = []  # Verwijzing naar nodes_class verwijderd

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
    
    def check_not_through_node(self, point_to_add: WirePoint) -> bool:
        return point_to_add.z != 0
    
    def check_not_return(self, point_to_add: WirePoint) -> bool:
        new_start = self.wirepoints[-1]    # last point in the current path
        new_end = point_to_add

        # 1) Check if new_start->new_end is the reverse of ANY segment in wirepoints
        for i in range(len(self.wirepoints) - 1):
            seg_start = self.wirepoints[i]
            seg_end = self.wirepoints[i + 1]
            # If the new segment exactly reverses an existing one:
            if seg_start == new_end and seg_end == new_start:
                return False

        # 2) Do the usual intersection checks
        temp_wirepoints = self.wirepoints + [new_end]
        for i in range(len(temp_wirepoints) - 2):
            if self._segments_intersect(
                temp_wirepoints[i], temp_wirepoints[i + 1],
                temp_wirepoints[-2], temp_wirepoints[-1]
            ):
                return False

        return True

    

    def _segments_intersect(self, p1, p2, p3, p4):
        """
        Helper to check if two line segments (p1-p2 and p3-p4) intersect.
        Returns True if they intersect, False otherwise.
        """

        def orientation(a, b, c):
            """Returns the orientation of three points."""
            val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
            if val == 0:
                return 0  # Collinear
            return 1 if val > 0 else 2  # Clockwise or counterclockwise

        def on_segment(a, b, c):
            """Check if point b lies on segment a-c."""
            return min(a.x, c.x) <= b.x <= max(a.x, c.x) and min(a.y, c.y) <= b.y <= max(a.y, c.y)

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases
        if o1 == 0 and on_segment(p1, p3, p2):
            return True
        if o2 == 0 and on_segment(p1, p4, p2):
            return True
        if o3 == 0 and on_segment(p3, p1, p4):
            return True
        if o4 == 0 and on_segment(p3, p2, p4):
            return True

        return False

    def pop_wire_point(self) -> None:
        self.wirepoints.pop(-2)
