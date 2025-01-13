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

# 4) Voorbeeld Wires aanmaken
wirelist = [Wire(nodes_list[netlist_list[0][0]-1], nodes_list[netlist_list[0][1]-1]), 
            Wire(nodes_list[netlist_list[1][0]-1], nodes_list[netlist_list[1][1]-1]), 
            Wire(nodes_list[netlist_list[2][0]-1], nodes_list[netlist_list[2][1]-1]), 
            Wire(nodes_list[netlist_list[3][0]-1], nodes_list[netlist_list[3][1]-1]), 
            Wire(nodes_list[netlist_list[4][0]-1], nodes_list[netlist_list[4][1]-1])]

wirepointslists = [[
    WirePoint(1, 5, 0),
    WirePoint(1, 5, 1),
    WirePoint(2, 5, 1),
    WirePoint(3, 5, 1),
    WirePoint(4, 5, 1),
    WirePoint(5, 5, 1),
    WirePoint(6, 5, 1),
    WirePoint(6, 5, 0)
], [
    WirePoint(1, 5, 0),
    WirePoint(1, 4, 0),
    WirePoint(2, 4, 0),
    WirePoint(3, 4, 0),
    WirePoint(4, 4, 0)
], [
    WirePoint(4, 4, 0),
    WirePoint(4, 3, 0),
    WirePoint(3, 3, 0),
    WirePoint(3, 2, 0),
    WirePoint(3, 1, 0)
], [
    WirePoint(6, 2, 0),
    WirePoint(6, 3, 0),
    WirePoint(6, 4, 0),
    WirePoint(6, 5, 0)
], [
    WirePoint(6, 2, 0),
    WirePoint(6, 1, 0),
    WirePoint(5, 1, 0),
    WirePoint(4, 1, 0),
    WirePoint(3, 1, 0)
]]

for wire in wirelist:
    for wirepointlist in wirepointslists:
        for wirepoint in wirepointlist:
            wire.add_wire_point(wirepoint)
            if not (grid.check_valid_addition(wire)):
                wire.pop_wire_point()

# 5) Wires registreren in het grid (zodat punt_dict en aantal_lijnen worden geüpdatet)
    grid.wire_toevoegen_dict(wire)

print(wirelist[0].wirepoints)

#haal de incorrecte kruisingen uit de dict.
for node in nodes_list:
    grid.nodes_uit_dictcount()

#)6 Voer een serie aan checks uit of de wires voldoen aan de door ons gestelde eisen.


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

plot_wires_3d(wirelist)

# 8) Totale kosten berekenen
print(f"The total cost for this grid is: {grid.kosten()}")
