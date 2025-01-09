import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from grid_class import Grid_3D
from nodes_class import importeer_nodes, Node
from connections_class import importeer_netlist
from wire_class import Wire, WirePoint

# 1) Grid aanmaken
x = 8
y = 7
grid = Grid_3D(x, y)

# 2) Nodes importeren en plaatsen
nodes_list = importeer_nodes('../gates&netlists/chip_0/print_0.csv')
for node in nodes_list:
    grid.plaats_node(node)

# 3) Netlist importeren
netlist_list = importeer_netlist('../gates&netlists/chip_0/netlist_1.csv')
# netlist_list is dan een lijst met (integer, integer), waar je
# iets mee kunt doen om Node's onderling te verbinden.

# 4) Voorbeeld Wires aanmaken
wire1 = Wire([
    WirePoint(1, 5, 0),
    WirePoint(1, 5, 1),
    WirePoint(2, 5, 1),
    WirePoint(3, 5, 1),
    WirePoint(4, 5, 1),
    WirePoint(5, 5, 1),
    WirePoint(6, 5, 1),
    WirePoint(6, 5, 0)
])
wire2 = Wire([
    WirePoint(1, 5, 0),
    WirePoint(1, 4, 0),
    WirePoint(2, 4, 0),
    WirePoint(3, 4, 0),
    WirePoint(4, 4, 0)
])
wire3 = Wire([
    WirePoint(4, 4, 0),
    WirePoint(4, 3, 0),
    WirePoint(3, 3, 0),
    WirePoint(3, 2, 0),
    WirePoint(3, 1, 0)
])
wire4 = Wire([
    WirePoint(6, 2, 0),
    WirePoint(6, 3, 0),
    WirePoint(6, 4, 0),
    WirePoint(6, 5, 0)
])
wire5 = Wire([
    WirePoint(6, 2, 0),
    WirePoint(6, 1, 0),
    WirePoint(5, 1, 0),
    WirePoint(4, 1, 0),
    WirePoint(3, 1, 0)
])

# 5) Wires registreren in het grid (zodat punt_dict en aantal_lijnen worden geüpdatet)
grid.wire_toevoegen_dict(wire1)
grid.wire_toevoegen_dict(wire2)
grid.wire_toevoegen_dict(wire3)
grid.wire_toevoegen_dict(wire4)
grid.wire_toevoegen_dict(wire5)


#haal de incorrecte kruisingen uit de dict.
for node in nodes_list:
    grid.nodes_uit_dictcount(node)

# 6) Eventueel check_wire() aanroepen
print("wire1 correct aangesloten?", wire1.check_wire())
print("wire2 correct aangesloten?", wire2.check_wire())
print("wire3 correct aangesloten?", wire3.check_wire())
print("wire4 correct aangesloten?", wire4.check_wire())
print("wire5 correct aangesloten?", wire5.check_wire())

# Check of de wires niet door nodes heenlopen
print("wire1 check_not_through_node() ->", wire1.check_not_through_node())
print("wire2 check_not_through_node() ->", wire2.check_not_through_node())
print("wire3 check_not_through_node() ->", wire3.check_not_through_node())
print("wire4 check_not_through_node() ->", wire4.check_not_through_node())
print("wire5 check_not_through_node() ->", wire5.check_not_through_node())

# 7) Voorbeeld: wires plotten in 3D
def plot_wires_3d(wires):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for wire in wires:
        xs = [p.x for p in wire.wirepoints]
        ys = [p.y for p in wire.wirepoints]
        zs = [p.z for p in wire.wirepoints]
        ax.plot(xs, ys, zs, marker='o')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

wires = [wire1, wire2, wire3, wire4, wire5]
plot_wires_3d(wires)

# 8) Totale kosten berekenen
print(f"The total cost for this grid is: {grid.kosten()}")
