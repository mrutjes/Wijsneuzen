import pandas as pd
from code.classes.nodes_class import Node
import itertools
import math

def import_netlist(csv_path) -> list[tuple[int, int]]:
    """
    Generates a list of tuples from the netlist csv file.
    """
    data = pd.read_csv(csv_path)
    return [
        (int(row['chip_a']), int(row['chip_b']))
        for _, row in data.iterrows()
    ]

def import_nodes(csv_path) -> list[Node]:
    """
    Imports nodes based on a csv file and returns a list of Node objects.
    """
    data = pd.read_csv(csv_path)

    return [
        Node(int(row['x']), int(row['y']))
        for _, row in data.iterrows()
    ]

def random_permutations(netlist, num_samples):
    """
    Generate a random sample of ⁠ num_samples ⁠ permutations from the netlist.
    """
    total_permutations = math.factorial(len(netlist))
    
    if num_samples >= total_permutations:
        return list(itertools.permutations(netlist))
    
    selected_permutations = set()
    while len(selected_permutations) < num_samples:
        perm = tuple(random.sample(netlist, len(netlist)))
        selected_permutations.add(perm)

    return list(selected_permutations)

def sort_netlist_busy_nodes(netlist):
    """
    Sorts a netlist based on how many times each node occurs in the netlist.
    
    Parameters:
    netlist (list of tuples): A list where each tuple represents a connection 
                              (e.g., [(node1, node2), (node2, node3), ...]).
    
    Returns:
    list of tuples: A sorted netlist where the nodes with the highest occurrences appear first.
    """
    node_counts = {}
    for connection in netlist:
        for node in connection:
            if node in node_counts:
                node_counts[node] += 1
            else:
                node_counts[node] = 1

    sorted_netlist = sorted(netlist, key=lambda x: (node_counts[x[0]] + node_counts[x[1]]), reverse=True)

    return sorted_netlist

def sort_netlist_distance(netlist, nodeslist):
    """
    Sorts a netlist based on the distance between two nodes for each connection.
    """
    num = 0
    dict = {}

    for connection in netlist:
        num += 1
        x_1 = nodeslist[connection[0] - 1].give_x()
        y_1 = nodeslist[connection[0] - 1].give_y()
        x_2 = nodeslist[connection[1] - 1].give_x()
        y_2 = nodeslist[connection[1] - 1].give_y()

        dist = abs(x_1 - x_2) + abs(y_1 - y_2)

        dict[(connection)] = dist

    sorted_netlist = sorted(netlist, key=lambda x: (dict[x]), reverse=True)

    return sorted_netlist

def sort_multiple_netlist_busy_nodes(netlist):
    """
    Generates all permutations of the netlist and sorts each permutation
    based on how many times each node occurs in the netlist.

    Parameters:
    netlist (list of tuples): A list where each tuple represents a connection.

    Returns:
    list of lists of tuples: All permutations of the netlist, sorted based on node usage.
    """
    # Count how many times each node occurs in the netlist
    node_counts = {}
    for connection in netlist:
        for node in connection:
            if node in node_counts:
                node_counts[node] += 1
            else:
                node_counts[node] = 1

    # Generate all permutations of the netlist
    permutations = itertools.permutations(netlist)

    # Sort each permutation based on the node counts
    sorted_permutations = []
    for perm in permutations:
        sorted_perm = sorted(perm, key=lambda x: (node_counts[x[0]] + node_counts[x[1]]), reverse=True)
        if sorted_perm not in sorted_permutations:
            sorted_permutations.append(sorted_perm)

    return sorted_permutations

def sort_multiple_netlist_distance(netlist, nodeslist):
    """
    Generates all permutations of the netlist and sorts each permutation
    based on the Manhattan distance between nodes for each connection.

    Parameters:
    netlist (list of tuples): A list where each tuple represents a connection.
    nodeslist (list of Node): A list of Node objects.

    Returns:
    list of lists of tuples: All permutations of the netlist, sorted based on distance.
    """
    distances = {}
    for connection in netlist:
        x_1 = nodeslist[connection[0] - 1].give_x()
        y_1 = nodeslist[connection[0] - 1].give_y()
        x_2 = nodeslist[connection[1] - 1].give_x()
        y_2 = nodeslist[connection[1] - 1].give_y()

        dist = abs(x_1 - x_2) + abs(y_1 - y_2)
        distances[connection] = dist

    permutations = itertools.permutations(netlist)

    sorted_permutations = []
    for perm in permutations:
        sorted_perm = sorted(perm, key=lambda x: distances[x], reverse=True)
        if sorted_perm not in sorted_permutations:
            sorted_permutations.append(sorted_perm)

    return sorted_permutations