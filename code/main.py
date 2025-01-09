from grid_class import Grid_3D
from nodes_class import Node, importeer_nodes
from connections_class import Wire, WirePoint, importeer_netlist
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#initialize the grid

x = 8
y = 7

grid = Grid_3D(x, y)

#initialize the nodes
nodes_list = importeer_nodes('../gates&netlists/chip_0/print_0.csv')

#put the nodes in the grid
for i in range(len(nodes_list)):
    grid.plaats_node(nodes_list[i])

#initialize the netlist
netlist_list = importeer_netlist('../gates&netlists/chip_0/netlist_1.csv')

#make wires from the netlist

#Zet de wirepoints in the dict

wire1 = Wire([WirePoint(1, 5, 0), WirePoint(1, 5, 1), WirePoint(2, 5, 1), WirePoint(3, 5, 1), WirePoint(4, 5, 1), WirePoint(5, 5, 1), WirePoint(6, 5, 1), WirePoint(6, 5, 0)])
wire2 = Wire([WirePoint(1, 5, 0), WirePoint(1, 4, 0), WirePoint(2, 4, 0), WirePoint(3, 4, 0), WirePoint(4, 4, 0)])
wire3 = Wire([WirePoint(4, 4, 0), WirePoint(4, 3, 0), WirePoint(3, 3, 0), WirePoint(3, 2, 0),WirePoint(3, 1, 0)])
wire4 = Wire([WirePoint(6, 2, 0), WirePoint(6, 3, 0), WirePoint(6, 4, 0), WirePoint(6, 5, 0)])
wire5 = Wire([WirePoint(6, 2, 0), WirePoint(6, 1, 0), WirePoint(5, 1, 0), WirePoint(4, 1, 0), WirePoint(3, 1, 0)])

#Check if the wires are wired
wire1.check_wire()
wire2.check_wire()
wire3.check_wire()
wire4.check_wire()
wire5.check_wire()

#Check if the wires are succesfully connected to the corrospoding notes
"""
wire1.check_connection()
wire2.check_connection()
wire3.check_connection()
wire4.check_connection()
wire5.check_connection()
"""
#visialize the grid using matplotlib
# Function to plot wires in 3D
def plot_wires_3d(wires):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for wire in wires:
        x = [point.x for point in wire.wirepoints]
        y = [point.y for point in wire.wirepoints]
        z = [point.z for point in wire.wirepoints]
        ax.plot(x, y, z, marker='o')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# List of wires
wires = [wire1, wire2, wire3, wire4, wire5]

# Visualize the grid using matplotlib
plot_wires_3d(wires)

#calculate cost