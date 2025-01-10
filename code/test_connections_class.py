import pytest

from nodes_class import Node
from wire_class import WirePoint, Wire


# ------------------------
# Tests for WirePoint
# ------------------------
def test_wirepoint_initialization():
    point = WirePoint(1, 2, 3)
    assert point.x == 1
    assert point.y == 2
    assert point.z == 3

def test_wirepoint_give_place():
    point = WirePoint(1, 2, 3)
    assert point.give_place() == (1, 2, 3)

def test_wirepoint_give_x():
    point = WirePoint(4, 5, 6)
    assert point.give_x() == 4

def test_wirepoint_give_y():
    point = WirePoint(4, 5, 6)
    assert point.give_y() == 5

def test_wirepoint_give_z():
    point = WirePoint(4, 5, 6)
    assert point.give_z() == 6


# ------------------------
# Tests for Wire
# ------------------------
def test_wire_initialization():
    """Test that the wire initializes correctly with start and end Node."""
    start_node = Node(0, 0)
    end_node = Node(1, 0)
    wire = Wire(start_node, end_node)

    assert len(wire.wirepoints) == 2, "Wire should initially have exactly 2 WirePoints."
    assert wire.wirepoints[0].give_place() == (0, 0, 0)
    assert wire.wirepoints[1].give_place() == (1, 0, 0)


def test_wire_add_wire_point():
    """
    Check that adding an intermediate WirePoint works as intended.
    The Wire constructor sets [start, end], 
    so adding one in the middle should expand the wire.
    """
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    # Initially: wirepoints = [(0, 0, 0), (2, 0, 0)]

    wire.add_wire_point(WirePoint(1, 0, 0))
    # Expected final: [(0,0,0), (1,0,0), (2,0,0)]
    assert len(wire.wirepoints) == 3
    assert wire.wirepoints[1].give_place() == (1, 0, 0), "Intermediate WirePoint was not inserted correctly."
    assert wire.wirepoints[-1].give_place() == (2, 0, 0), "End WirePoint should remain (end_node.x, end_node.y, 0)."


def test_wire_pop_wire_point():
    """
    Check that popping the second-to-last WirePoint (the 'middle') 
    reduces the wire back to the original start/end points.
    """
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    # Initially: [(0,0,0), (2,0,0)]

    wire.add_wire_point(WirePoint(1, 0, 0))  
    # Now: [(0,0,0), (1,0,0), (2,0,0)]

    wire.pop_wire_point()
    # Should remove the point before the last => back to [(0,0,0), (2,0,0)]
    assert len(wire.wirepoints) == 2, "Pop should restore the wire to its original 2 points."
    assert wire.wirepoints[0].give_place() == (0, 0, 0)
    assert wire.wirepoints[1].give_place() == (2, 0, 0)


def test_wire_check_wire_valid():
    """
    Build a wire with valid 1-step increments 
    so check_wire() should return True.
    """
    start_node = Node(0, 0)
    end_node = Node(3, 0)
    wire = Wire(start_node, end_node)
    # Currently: [(0,0,0), (3,0,0)] => Not valid steps 
    # We'll add the missing intermediate steps:
    wire.add_wire_point(WirePoint(1, 0, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))
    # Now wirepoints = [
    #   (0,0,0),  # from start_node
    #   (1,0,0),  
    #   (2,0,0),  
    #   (3,0,0)   # from end_node
    # ]
    assert wire.check_wire() is True, "Wire should be valid with consecutive 1-step increments."


def test_wire_check_wire_invalid():
    """
    Build a wire with a gap larger than 1 between consecutive WirePoints 
    so check_wire() should return False.
    """
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    # By default: [(0,0,0), (2,0,0)]
    # We'll add a wire point that doesn't help connect them properly:
    wire.add_wire_point(WirePoint(0, 1, 0))
    # => wirepoints = [(0,0,0), (0,1,0), (2,0,0)]
    # The jump from (0,1,0) to (2,0,0) is 2 in x.
    assert wire.check_wire() is False, "Wire has a 2-step gap, so it should be invalid."


def test_wire_check_connection():
    """
    check_connection() should verify the first WP is at (start.x, start.y)
    and the last WP is at (end.x, end.y), or vice versa.
    """
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    # wirepoints => [(0,0,0), (2,0,0)]
    assert wire.check_connection() is True, "Connection should match start_node -> end_node."

    # Let's manually reverse them and see if that still passes:
    # In this implementation, the wire always starts with start_node, 
    # so for a 'reversed' check, you'd effectively re-init a wire 
    # with reversed start/end if you want that scenario. 
    # But the method covers both directions.


def test_check_not_through_node_no_middle_node():
    """
    If the wire doesn't pass through any node in the middle, 
    check_not_through_node() should return True.
    """
    start_node = Node(0, 0)
    end_node = Node(3, 0)
    wire = Wire(start_node, end_node)
    # wirepoints => [(0,0,0), (3,0,0)] 
    # Insert (1,0,0) and (2,0,0) so we have a 'middle' path:
    wire.add_wire_point(WirePoint(1, 0, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))
    # wirepoints => [(0,0,0), (1,0,0), (2,0,0), (3,0,0)]

    # Suppose we have nodes at other places:
    wire.nodes = [Node(1, 1), Node(2, 2)]
    # None of those is at the middle wirepoints (1,0) or (2,0).
    assert wire.check_not_through_node() is True


def test_check_not_through_node_intersect_in_middle():
    """
    If there's a node exactly at a middle wirepoint (z=0),
    check_not_through_node() should return False.
    """
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    # wirepoints => [(0,0,0), (2,0,0)]

    # Insert a middle point => (1,0,0)
    wire.add_wire_point(WirePoint(1, 0, 0))
    # wirepoints => [(0,0,0), (1,0,0), (2,0,0)]

    # There's a node at (1,0):
    wire.nodes = [Node(1, 0)]
    # Middle index is 1 => that matches the node => should return False.
    assert wire.check_not_through_node() is False


def test_check_not_through_node_start_or_end():
    """
    A node at the start or end doesn't invalidate the wire. 
    check_not_through_node() should still return True.
    """
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    # wirepoints => [(0,0,0), (2,0,0)]

    # Let's place a node exactly at start (0,0) and end (2,0).
    wire.nodes = [Node(0, 0), Node(2, 0)]
    # The method ignores the first and last wirepoint when checking intersection => True.
    assert wire.check_not_through_node() is True


def test_check_not_through_node_minimal_wire():
    """
    If the wire has only two points (start and end), 
    there's no 'middle' to intersect with a node => always True.
    """
    start_node = Node(0, 0)
    end_node = Node(1, 0)
    wire = Wire(start_node, end_node)
    # wirepoints => [(0,0,0), (1,0,0)]
    # Even if there's a node on (0,0) or (1,0), 
    # it's allowed since those are start/end.
    wire.nodes = [Node(0, 0), Node(1, 0)]
    assert wire.check_not_through_node() is True
