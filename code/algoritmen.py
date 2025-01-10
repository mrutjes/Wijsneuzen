import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import heapq

from grid_class import Grid_3D
from nodes_class import Node
from connections_class import importeer_netlist
from wire_class import Wire, WirePoint
import csv


def importeer_nodes(filepath):
    """
    Importeer nodes vanuit een CSV en retourneer een dictionary met node-ID als sleutel
    en (x, y, z) als waarde.
    """
    nodes_dict = {}
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Sla de header over
        for row in reader:
            node_id = int(row[0])
            x = int(row[1])
            y = int(row[2])
            z = 0  # Aangenomen dat nodes op z = 0 liggen
            nodes_dict[node_id] = (x, y, z)
    return nodes_dict


class PathFinder:
    """
    Pathfinding class using A* algorithm
    """

    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, end):
        """
        Find a path from start to end using A* algorithm
        """
        start_wp = WirePoint(*start)
        end_wp = WirePoint(*end)

        open_set = []
        heapq.heappush(open_set, (0, start_wp))
        came_from = {}
        cost_so_far = {start_wp: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end_wp:
                return self.reconstruct_path(came_from, start_wp, end_wp)

            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                new_cost = cost_so_far[current] + 1  # Assume uniform cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, end_wp)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

        return None

    def reconstruct_path(self, came_from, start, end):
        """
        Reconstruct the path from start to end
        """
        path = [end]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        path.reverse()
        return path

    def heuristic(self, a, b):
        """
        Heuristic function (Manhattan distance)
        """
        return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


# 1) Grid aanmaken
x = 8
y = 7
grid = Grid_3D(x, y)

# 2) Nodes importeren en plaatsen
for node_id, (x, y, z) in nodes_dict.items():
    node = Node(x, y, z)  # Maak een Node-object met x, y, en z
    grid.plaats_node(node)


# 3) Netlist importeren
netlist_list = importeer_netlist('../gates&netlists/chip_0/netlist_1.csv')

# 4) PathFinder gebruiken
pathfinder = PathFinder(grid)
for connection in netlist_list:
    node_a_id, node_b_id = connection
    node_a_coords = nodes_dict.get(node_a_id)
    node_b_coords = nodes_dict.get(node_b_id)

    if node_a_coords is None or node_b_coords is None:
        print(f"Error: One of the nodes in connection {connection} does not exist.")
        continue

    # Vind een pad tussen de nodes
    path = pathfinder.find_path(node_a_coords, node_b_coords)
    if path:
        wire = Wire(path)
        grid.wire_toevoegen_dict(wire)
    else:
        print(f"No valid path found for connection between {node_a_id} and {node_b_id}")

# 5) Wires plotten in 3D
def plot_wires_3d(wires):
    """
    Plot the wires in a 3D graph
    """
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


# Plot de wires
plot_wires_3d(grid.wires)

# 6) Totale kosten berekenen
print(f"The total cost for this grid is: {grid.kosten()}")
