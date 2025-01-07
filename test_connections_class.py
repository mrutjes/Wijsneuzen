import pytest
from connections_class import WirePoint, Wire

# Test WirePoint class
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

# Test Wire class
def test_wire_initialization():
    points = [WirePoint(0, 0, 0), WirePoint(1, 0, 0)]
    wire = Wire(points)
    assert wire.wirepoints == points

def test_wire_check_connection_valid():
    points = [
        WirePoint(0, 0, 0),
        WirePoint(1, 0, 0),
        WirePoint(1, 1, 0),
        WirePoint(1, 1, 1)
    ]
    wire = Wire(points)
    assert wire.check_connection() is True

def test_wire_check_connection_invalid():
    points = [
        WirePoint(0, 0, 0),
        WirePoint(2, 0, 0),  # Not connected directly
        WirePoint(1, 1, 0)
    ]
    wire = Wire(points)
    assert wire.check_connection() is False

def test_wire_check_connection_edge_case_single_point():
    points = [WirePoint(0, 0, 0)]
    wire = Wire(points)
    assert wire.check_connection() is True  # Single point is trivially connected

def test_wire_check_connection_disjoint_points():
    points = [
        WirePoint(0, 0, 0),
        WirePoint(1, 0, 0),
        WirePoint(3, 0, 0)  # Disjoint from the previous points
    ]
    wire = Wire(points)
    assert wire.check_connection() is False

def test_wire_check_connection_3d_connections():
    points = [
        WirePoint(0, 0, 0),
        WirePoint(0, 0, 1),
        WirePoint(0, 1, 1),
        WirePoint(1, 1, 1)
    ]
    wire = Wire(points)
    assert wire.check_connection() is True