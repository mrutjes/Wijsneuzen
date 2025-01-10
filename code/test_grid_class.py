import pytest
from wire_class import Wire, WirePoint
from nodes_class import Node
from grid_class import Grid_3D

@pytest.fixture
def grid():
    """Maakt een Grid_3D object met afmeting 10x10."""
    return Grid_3D(10, 10)

def test_init_grid(grid):
    """
    Controleren dat het Grid_3D object correct is geïnitieerd:
    - Afmetingen kloppen
    - Hoogte is 8
    - Dictionary heeft de juiste grootte
    - Alle waarden in de dictionary zijn 0
    """
    assert grid.n == 10
    assert grid.m == 10
    assert grid.hoogte == 8
    assert len(grid.punt_dict) == 10 * 10 * 8
    assert all(value == 0 for value in grid.punt_dict.values())

def test_plaats_node_ok(grid):
    """
    Test of 'plaats_node' geen error gooit binnen geldige grid-afmetingen.
    """
    node = Node(x=3, y=3)
    grid.plaats_node(node)  # Zou geen error moeten opleveren

def test_plaats_node_out_of_bounds(grid):
    """
    Controleren dat er een IndexError wordt gegooid 
    als de Node buiten de grid-afmetingen valt.
    """
    node = Node(x=99, y=3)  # Buiten x-dimensie
    with pytest.raises(IndexError):
        grid.plaats_node(node)

def test_wire_toevoegen_dict(grid):
    """
    Test of wire_toevoegen_dict correct omgaat met een wire die 
    start_node=(0,0) en end_node=(0,2) heeft, met een tussenpunt (0,1).
    Controleer ook of aantal_lijnen en punt_dict worden geüpdatet.
    """
    # Maak een wire van (0,0) -> (0,2), en voeg één tussenpunt (0,1) toe
    wire = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=2)
    )
    wire.add_wire_point(WirePoint(0, 1, 0))  # Tussenpunt

    # Nu heeft wire.wirepoints: [(0,0,0), (0,1,0), (0,2,0)]
    grid.wire_toevoegen_dict(wire)

    # We hebben 3 punten, dus 2 lijnstukjes
    assert grid.aantal_lijnen == 2

    # Iedere grid-positie hoort nu op 1 te staan
    assert grid.punt_dict[(0, 0, 0)] == 1
    assert grid.punt_dict[(0, 1, 0)] == 1
    assert grid.punt_dict[(0, 2, 0)] == 1

def test_wire_toevoegen_met_wirepoints(grid):
    """
    Test of wire_toevoegen_dict correct omgaat met meerdere tussenpunten.
    We starten bij (1,5) en eindigen bij (6,5), met diverse tussenpunten op z=1.
    Controleer ook of aantal_lijnen en punt_dict worden geüpdatet.
    """
    wire = Wire(
        start_node=Node(x=1, y=5),
        end_node=Node(x=6, y=5)
    )
    # Voeg tussenpunten toe op z=1:
    wire.add_wire_point(WirePoint(1, 5, 1))
    wire.add_wire_point(WirePoint(2, 5, 1))
    wire.add_wire_point(WirePoint(3, 5, 1))
    wire.add_wire_point(WirePoint(4, 5, 1))
    wire.add_wire_point(WirePoint(5, 5, 1))
    wire.add_wire_point(WirePoint(6, 5, 1))

    # Nu heeft wire in totaal 8 wirepoints:
    # (1,5,0) - (1,5,1) - (2,5,1) - (3,5,1) - (4,5,1) - (5,5,1) - (6,5,1) - (6,5,0)
    grid.wire_toevoegen_dict(wire)
    
    # 8 punten -> 7 lijnstukjes
    assert grid.aantal_lijnen == 7

    # Elke betrokken coordinate zou nu 1 in punt_dict moeten hebben
    for point in wire.wirepoints:
        assert (point.x, point.y, point.z) in grid.punt_dict
        assert grid.punt_dict[(point.x, point.y, point.z)] == 1


def check_valid_addition(self, point_to_add, current_wire):
    from wire_class import WirePoint

    # Remove or comment out the problematic line:
    # if (wire.wirepoints[i+1] == point_to_add and wire.wirepoints[i] == current_wire.wirepoints[-2]):
    #     return False

    if point_to_add not in self.punt_dict:
        return False

    for wire in self.wires:
        for i in range(len(wire.wirepoints) - 1):
            if (wire.wirepoints[i+1] == point_to_add and wire.wirepoints[i] == current_wire.wirepoints[-2]):
                return False

    if not current_wire.check_not_through_node(point_to_add):
        return False
    if not current_wire.check_not_return(point_to_add):
        return False

    return True

def test_totaal_kruisingen(grid):
    """
    Test de methode totaal_kruisingen:
    - Als twee wires hetzelfde gridpunt delen, ontstaat er een kruising.
    """
    wire1 = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    wire2 = Wire(
        start_node=Node(x=0, y=1),  # deelt 'wirepoints' met wire1 eind
        end_node=Node(x=1, y=1)
    )

    grid.wire_toevoegen_dict(wire1)
    grid.wire_toevoegen_dict(wire2)

    # wire1 en wire2 delen het punt (0,1,0) -> kruising = 1
    assert grid.totaal_kruisingen() == 1

def test_kosten(grid):
    """
    Test de methode kosten:
    - kosten = (kruisingen * 300) + aantal_lijnen
    """
    # Twee wires met 1 gedeeld punt
    wire1 = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    wire2 = Wire(
        start_node=Node(x=0, y=1),
        end_node=Node(x=1, y=1)
    )

    grid.wire_toevoegen_dict(wire1)  # levert 1 lijnstuk op
    grid.wire_toevoegen_dict(wire2)  # levert nog 1 lijnstuk op

    # Kruisingen: 1 (punt (0,1,0) gedeeld door 2 wires)
    # Aantal lijnstukken: 2
    # kosten = 1*300 + 2 = 302
    assert grid.kosten() == 302
