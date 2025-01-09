import pytest
from wire_class import WirePoint, Wire
from nodes_class import Node

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
    assert wire.check_wire() is True

def test_wire_check_connection_invalid():
    points = [
        WirePoint(0, 0, 0),
        WirePoint(2, 0, 0),  # Not connected directly
        WirePoint(1, 1, 0)
    ]
    wire = Wire(points)
    assert wire.check_wire() is False

def test_wire_check_connection_edge_case_single_point():
    points = [WirePoint(0, 0, 0)]
    wire = Wire(points)
    assert wire.check_wire() is True  # Single point is trivially connected

def test_wire_check_connection_disjoint_points():
    points = [
        WirePoint(0, 0, 0),
        WirePoint(1, 0, 0),
        WirePoint(3, 0, 0)  # Disjoint from the previous points
    ]
    wire = Wire(points)
    assert wire.check_wire() is False

def test_wire_check_connection_3d_connections():
    points = [
        WirePoint(0, 0, 0),
        WirePoint(0, 0, 1),
        WirePoint(0, 1, 1),
        WirePoint(1, 1, 1)
    ]
    wire = Wire(points)
    assert wire.check_wire() is True

def test_wire_check_node_connection():
    node1 = Node(0, 0)
    node2 = Node(1, 0)
    node3 = Node(2, 0)

    wire = Wire([node1, node2])

    assert wire.check_connection(node1, node2) is True  # Valid connection
    assert wire.check_connection(node2, node1) is True  # Valid reversed connection
    assert wire.check_connection(node1, node3) is False  # Invalid connection
    assert wire.check_connection(node3, node2) is False  # Invalid connection

def test_check_not_through_node_no_intersection():
    """
    Controleer dat de methode True teruggeeft als er géén node in het midden ligt.
    """
    # Stel een wire samen met vier punten.
    #  De node-locaties komen niet overeen met de middelste WirePoints.
    wirepoints = [
        WirePoint(0, 0, 0),
        WirePoint(1, 0, 0),
        WirePoint(2, 0, 0),
        WirePoint(3, 0, 0)
    ]
    # Maak Node-objecten op andere plekken
    nodes = [
        Node(5, 5),
        Node(2, 2)
    ]
    wire = Wire(wirepoints)
    # Voeg je nodes toe aan wire.nodes (zoals je code zelf aangeeft)
    wire.nodes = nodes

    assert wire.check_not_through_node() == True, (
        "Wire zou géén node in het midden moeten kruisen."
    )


def test_check_not_through_node_intersect_in_middle():
    """
    Controleer dat de methode False teruggeeft als er wél een node in het midden ligt.
    """
    wirepoints = [
        WirePoint(0, 0, 0),
        WirePoint(1, 0, 0),  # middelste
        WirePoint(2, 0, 0)
    ]
    # De node valt precies samen met de middelste wirepoint
    nodes = [Node(1, 0)]
    
    wire = Wire(wirepoints)
    wire.nodes = nodes

    assert wire.check_not_through_node() == False, (
        "Wire gaat door een node in het midden, dus verwacht False."
    )


def test_check_not_through_node_start_or_end():
    """
    Controleer dat bij een node op het start- of eindpunt
    de methode alsnog True geeft (want daar mag hij liggen).
    """
    wirepoints = [
        WirePoint(0, 0, 0),
        WirePoint(1, 0, 0),
        WirePoint(2, 0, 0)
    ]
    # Node op de eerste en laatste wirepoint
    nodes = [
        Node(0, 0),
        Node(2, 0)
    ]
    wire = Wire(wirepoints)
    wire.nodes = nodes

    assert wire.check_not_through_node() == True, (
        "Nodes liggen alleen op de start- en eindwirepoint, dus verwacht True."
    )


def test_check_not_through_node_minimal_wire():
    """
    Controleer een wire die slechts twee punten heeft.
    Daar is geen 'middenstuk', dus het zou altijd True moeten returnen.
    """
    wirepoints = [
        WirePoint(0, 0, 0),
        WirePoint(1, 0, 0)
    ]
    # Zelfs als er hier nodes op 0,0 en 1,0 zijn,
    # maakt het niet uit, want dat zijn start- en eindpunten.
    nodes = [Node(0, 0), Node(1, 0)]
    
    wire = Wire(wirepoints)
    wire.nodes = nodes

    assert wire.check_not_through_node() == True, (
        "Wire met slechts twee punten heeft geen 'midden' om te kruisen."
    )