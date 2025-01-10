import pytest
from wire_class import Wire, WirePoint
from nodes_class import Node
from grid_class import Grid_3D

@pytest.fixture
def grid():
    """Maakt een Grid_3D object met afmeting 10x10."""
    return Grid_3D(10, 10)

def test_init_grid(grid):
    """Controleren dat alle waarden in de dict 0 zijn"""
    assert grid.n == 10
    assert grid.m == 10
    assert grid.hoogte == 8
    assert len(grid.punt_dict) == 10 * 10 * 8
    assert all(value == 0 for value in grid.punt_dict.values())

def test_plaats_node_ok(grid):
    """
    Test of plaats_node een node correct plaatst.
    """
    node = Node(x=3, y=3)
    grid.plaats_node(node)

def test_plaats_node_out_of_bounds(grid):
    """buiten de x-dimensie, kijken voor indexerror"""
    node = Node(x=99, y=3)
    with pytest.raises(IndexError):
        grid.plaats_node(node)

def test_wire_toevoegen_dict(grid):
    """
    Test of wire_toevoegen_dict correct omgaat met wirepoints
    en of aantal_lijnen en punt_dict geüpdatet worden.
    """
    # Stel een wire samen met drie punten -> twee lijnstukjes
    wire = Wire([
        Node(x=0, y=0),
        Node(x=0, y=1),
        Node(x=0, y=2),
    ])
    grid.wire_toevoegen_dict(wire)
    # Verwacht dat er 2 lijnstukjes zijn toegevoegd
    assert grid.aantal_lijnen == 2
    # Controleer dat de punt_dict op de juiste punten is verhoogd
    assert grid.punt_dict[(0, 0, 0)] == 1
    assert grid.punt_dict[(0, 1, 0)] == 1
    assert grid.punt_dict[(0, 2, 0)] == 1

@pytest.fixture
def grid():
    """Maak een Grid_3D-object met afmetingen 10x10."""
    return Grid_3D(10, 10)

def test_wire_toevoegen_met_wirepoints(grid):
    """
    Test of wire_toevoegen_dict correct omgaat met WirePoints 
    en of aantal_lijnen en punt_dict worden geüpdatet.
    """
    wire = Wire([
        WirePoint(1, 5, 0),
        WirePoint(1, 5, 1),
        WirePoint(2, 5, 1),
        WirePoint(3, 5, 1),
        WirePoint(4, 5, 1),
        WirePoint(5, 5, 1),
        WirePoint(6, 5, 1),
        WirePoint(6, 5, 0)
    ])
    
    # Toevoegen aan het grid
    grid.wire_toevoegen_dict(wire)
    
    # Aantal lijnstukjes = aantal wirepoints - 1
    assert grid.aantal_lijnen == 7
    
    # Controleer of in de punt_dict de teller voor elk wirepunt is verhoogd
    # en dat de coördinaten binnen de bounds blijven.
    for wp in wire.wirepoints:
        assert (wp.x, wp.y, wp.z) in grid.punt_dict
        assert grid.punt_dict[(wp.x, wp.y, wp.z)] == 1