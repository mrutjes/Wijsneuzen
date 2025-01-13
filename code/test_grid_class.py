# Filename: test_grid.py

import pytest
from grid_class import Grid_3D
from nodes_class import Node
from wire_class import Wire, WirePoint


@pytest.fixture
def grid():
    """
    Creëert een Grid_3D object met afmeting 10x10.
    """
    return Grid_3D(n=10, m=10)


def test_init_grid(grid):
    """
    Test of het Grid_3D object correct is geïnitieerd:
      - n=10, m=10, hoogte=8
      - Alle (x,y,z)-posities in punt_dict zijn 0
    """
    assert grid.n == 10
    assert grid.m == 10
    assert grid.hoogte == 8
    assert len(grid.punt_dict) == 10 * 10 * 8
    assert all(value == 0 for value in grid.punt_dict.values())


def test_plaats_node_in_bounds(grid):
    """
    Test of 'plaats_node' geen error gooit als de node binnen de grid ligt.
    """
    node = Node(x=3, y=4)
    # Moet geen error geven
    grid.plaats_node(node, z=0)


def test_plaats_node_out_of_bounds(grid):
    """
    Controleert dat er een IndexError wordt gegooid als de Node buiten de grid valt.
    """
    node = Node(x=99, y=99)  # Ruim buiten de 10x10
    with pytest.raises(IndexError):
        grid.plaats_node(node, z=0)


def test_wire_toevoegen_dict(grid):
    """
    Test of wire_toevoegen_dict correct omgaat met een wire
    die (0,0)->(0,2) loopt met tussenpunt (0,1).
    """
    wire = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=2)
    )
    # We gaan ervan uit dat Wire in z=0 start en eindigt,
    # en dat add_wire_point de z-coordinaat verwerkt.
    wire.add_wire_point(WirePoint(0, 1, 0))  # tussenpunt
    # wire.wirepoints: [(0,0,0), (0,1,0), (0,2,0)]
    
    grid.wire_toevoegen_dict(wire)
    # We hebben 3 punten, dus 2 lijnstukjes
    assert grid.aantal_lijnen == 2
    # Iedere gebruikte (x,y,z) moet nu 1 in punt_dict zijn
    for point in wire.wirepoints:
        assert grid.punt_dict[(point.x, point.y, point.z)] == 1


def test_wire_toevoegen_met_meerdere_tussenpunten(grid):
    """
    Test of wire_toevoegen_dict correct omgaat met meerdere tussenpunten.
    """
    wire = Wire(
        start_node=Node(x=1, y=5),
        end_node=Node(x=6, y=5)
    )
    # Voeg tussenpunten toe (in z=1, bijvoorbeeld):
    wire.add_wire_point(WirePoint(1, 5, 1))
    wire.add_wire_point(WirePoint(2, 5, 1))
    wire.add_wire_point(WirePoint(3, 5, 1))
    wire.add_wire_point(WirePoint(4, 5, 1))
    wire.add_wire_point(WirePoint(5, 5, 1))
    wire.add_wire_point(WirePoint(6, 5, 1))
    # wire.wirepoints: (1,5,0)->(1,5,1)->(2,5,1)->...->(6,5,1)->(6,5,0)

    grid.wire_toevoegen_dict(wire)
    # 8 punten -> 7 lijnsegmenten
    assert grid.aantal_lijnen == 7
    for point in wire.wirepoints:
        assert grid.punt_dict[(point.x, point.y, point.z)] == 1


def test_check_valid_addition_outside_grid(grid):
    """
    Test check_valid_addition:
    - Verwacht False als het 'op één na laatste' punt buiten de grid valt.
      In de code wordt gecheckt of current_wire.wirepoints[-2] in punt_dict zit.
    """
    # Maak een wire met 2 punten. Het op één na laatste punt is
    # wire.wirepoints[-2], dus we hebben minstens 2 punten nodig.
    wire = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    # Forceer het op één na laatste punt buiten de grid (bijv. x=15)
    wire.wirepoints = [
        WirePoint(0, 0, 0),
        WirePoint(15, 0, 0)  # buiten de 10x10 in x-richting
    ]
    assert grid.check_valid_addition(wire) is False


def test_check_valid_addition_collision(grid):
    """
    Test check_valid_addition:
    - Verwacht False als het te vormen segment een bestaand segment 'kruist'.
    """
    # Voeg een bestaande wire toe in de grid
    wire1 = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    wire1.add_wire_point(WirePoint(0, 1, 0))
    # wire1.wirepoints: [(0,0,0), (0,1,0), (0,1,0)???]
    # Let op, meestal zou je end_node.x, end_node.y, etc. 
    # tot (0,1,0) maken, maar pas het aan zoals je wire_class werkt.
    grid.wires.append(wire1)

    # current_wire dat hetzelfde segment probeert te gebruiken
    # We zorgen dat wire2.wirepoints[-3] en [-2] precies
    # het segment (0,0,0)->(0,1,0) zouden 'herhalen'.
    wire2 = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=2)
    )
    wire2.wirepoints = [
        WirePoint(0, 0, 0),
        WirePoint(0, 1, 0),
        WirePoint(0, 2, 0),
    ]
    # De code checkt segment collision met last_point = wire2.wirepoints[-3]
    # en point_to_add = wire2.wirepoints[-2]. Dat is (0,0,0)->(0,1,0).

    assert grid.check_valid_addition(wire2) is False


def test_check_valid_addition_through_node(grid):
    """
    Test check_valid_addition:
    - Verwacht False als current_wire.check_not_through_node() False teruggeeft.
    """
    wire = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    # Zet een minimal wirepoints-lijst zodat -2 en -3 bestaan
    wire.wirepoints = [WirePoint(0,0,0), WirePoint(0,1,0), WirePoint(0,2,0)]

    # Mock de methode check_not_through_node() op wire:
    wire.check_not_through_node = lambda: False
    # check_not_return() True, zodat die test niet blokkeert
    wire.check_not_return = lambda: True

    assert grid.check_valid_addition(wire) is False


def test_check_valid_addition_return_on_itself(grid):
    """
    Test check_valid_addition:
    - Verwacht False als current_wire.check_not_return() False geeft.
    """
    wire = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    wire.wirepoints = [WirePoint(0,0,0), WirePoint(0,1,0), WirePoint(0,2,0)]

    wire.check_not_through_node = lambda: True
    wire.check_not_return = lambda: False

    assert grid.check_valid_addition(wire) is False


def test_check_valid_addition_valid(grid):
    """
    Test check_valid_addition:
    - Verwacht True als alle checks slagen (in-grid, geen collision, 
      niet through node, niet return on itself).
    """
    wire = Wire(
        start_node=Node(x=1, y=1),
        end_node=Node(x=4, y=4)
    )
    wirepoints = [
        WirePoint(1,2,0),
        WirePoint(1,3,0),
        WirePoint(2,3,0),
        WirePoint(3,3,0),
        WirePoint(4,3,0),
    ]
    for wirepoint in wirepoints:
        wire.add_wire_point(wirepoint)

    assert grid.check_valid_addition(wire) is True


def test_totaal_kruisingen(grid):
    """
    Test de methode totaal_kruisingen():
    - Plaats twee wires die een punt delen => 1 kruising
    """
    w1 = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    w1.wirepoints = [WirePoint(0,0,0), WirePoint(0,1,0)]

    w2 = Wire(
        start_node=Node(x=0, y=1),
        end_node=Node(x=1, y=1)
    )
    w2.wirepoints = [WirePoint(0,1,0), WirePoint(1,1,0)]

    grid.wire_toevoegen_dict(w1)
    grid.wire_toevoegen_dict(w2)
    # (0,1,0) wordt door beide wires gebruikt => 
    # kruisingen = aantal_keer_te_veel = (2 - 1) = 1
    assert grid.totaal_kruisingen() == 1


def test_kosten(grid):
    """
    Test de methode kosten():
    - Kosten = (kruisingen * 300) + aantal_lijnen
    """
    w1 = Wire(
        start_node=Node(x=0, y=0),
        end_node=Node(x=0, y=1)
    )
    w1.wirepoints = [WirePoint(0,0,0), WirePoint(0,1,0)]

    w2 = Wire(
        start_node=Node(x=0, y=1),
        end_node=Node(x=1, y=1)
    )
    w2.wirepoints = [WirePoint(0,1,0), WirePoint(1,1,0)]

    grid.wire_toevoegen_dict(w1)  # 1 lijnsegment
    grid.wire_toevoegen_dict(w2)  # 1 lijnsegment => totaal 2

    # Er is 1 kruising (punt (0,1,0) gebruikt door beide wires)
    # Kosten = 1*300 + 2 = 302
    assert grid.kosten() == 302
