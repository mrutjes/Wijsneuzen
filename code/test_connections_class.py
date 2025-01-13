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

def test_wirepoint_individual_coordinates():
    point = WirePoint(4, 5, 6)
    assert point.give_x() == 4
    assert point.give_y() == 5
    assert point.give_z() == 6


# ------------------------
# Tests for Wire
# ------------------------
def test_wire_initialization():
    """Test that a wire initializes correctly with start and end nodes."""
    start_node = Node(0, 0)
    end_node = Node(1, 0)
    wire = Wire(start_node, end_node)

    assert len(wire.wirepoints) == 2
    assert wire.wirepoints[0].give_place() == (0, 0, 0)
    assert wire.wirepoints[1].give_place() == (1, 0, 0)


def test_wire_add_wire_point():
    """Check if a wire can correctly add an intermediate WirePoint."""
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)

    wire.add_wire_point(WirePoint(1, 0, 0))
    assert len(wire.wirepoints) == 3
    assert wire.wirepoints[1].give_place() == (1, 0, 0)


def test_wire_pop_wire_point():
    """Test if removing the last intermediate WirePoint works."""
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    wire.add_wire_point(WirePoint(1, 0, 0))

    wire.pop_wire_point()
    assert len(wire.wirepoints) == 2
    assert wire.wirepoints[-1].give_place() == (2, 0, 0)


def test_wire_check_wire_valid():
    """Test if a wire with valid consecutive points passes check_wire()."""
    start_node = Node(0, 0)
    end_node = Node(3, 0)
    wire = Wire(start_node, end_node)
    wire.add_wire_point(WirePoint(1, 0, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))

    assert wire.check_wire() is True


def test_wire_check_wire_invalid():
    """Test if a wire with a gap in WirePoints fails check_wire()."""
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    wire.add_wire_point(WirePoint(0, 1, 0))

    assert wire.check_wire() is False


def test_wire_check_connection():
    """Test if check_connection() validates correct start and end points."""
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)

    assert wire.check_connection() is True


def test_wire_check_not_through_node():
    """Test if a wire correctly detects intersection with a node."""
    start_node = Node(0, 0)
    end_node = Node(2, 0)
    wire = Wire(start_node, end_node)
    wire.nodes = [Node(1, 0), Node(2, 0)]
    wire.add_wire_point(WirePoint(1, 0, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))

    assert wire.check_not_through_node() is False

def test_wire_check_not_return_valid():
    start_node = Node(0, 0)
    end_node = Node(3, 0)
    wire = Wire(start_node, end_node)
    wire.add_wire_point(WirePoint(1, 0, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))
    wire.add_wire_point(WirePoint(1, 0, 0))

    assert wire.check_not_return() is False

def test_wire_check_not_return_invalid():
    start_node = Node(0, 0)
    end_node = Node(3, 0)
    wire = Wire(start_node, end_node)
    wire.add_wire_point(WirePoint(1, 0, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))

    # Invalid path, turns back on itself
    assert wire.check_not_return() is True

def test_not_return_but_kruising():
    start_node = Node(0, 0)
    end_node = Node(3, 0)
    wire = Wire(start_node, end_node)
    wire.add_wire_point(WirePoint(1, 0, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))
    wire.add_wire_point(WirePoint(2, 1, 0))
    wire.add_wire_point(WirePoint(2, 2, 0))
    wire.add_wire_point(WirePoint(2, 0, 0))

    assert wire.check_not_return() is True
