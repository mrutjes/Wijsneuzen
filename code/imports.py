import pandas as pd
from code.classes.nodes_class import Node
import itertools
import math
import random

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

    sorted_netlist = sorted(netlist, key=lambda x: (dict[x]), reverse=False)

    return sorted_netlist

def sort_multiple_netlist_busy_nodes(netlist, num_variations = 100):
    """
    Genereer verschillende gesorteerde versies van de netlist, gebaseerd op de frequentie van nodes.
    Als meerdere verbindingen dezelfde frequentie hebben, worden ze willekeurig herschikt.

    Parameters:
    netlist (list of tuples): Een lijst van verbindingen, waarbij elke tuple twee nodes verbindt.
    num_variations (int): Aantal gesorteerde versies van de netlist die gegenereerd moeten worden.

    Returns:
    list of lists of tuples: Een lijst van gesorteerde netlists.
    """
    # Tel hoe vaak elke node voorkomt in de netlist
    node_counts = {}
    for connection in netlist:
        for node in connection:
            node_counts[node] = node_counts.get(node, 0) + 1

    # Sorteer de netlist op basis van de frequentie van de nodes
    sorted_netlist = sorted(netlist, key=lambda x: (node_counts[x[0]] + node_counts[x[1]]), reverse=True)

    # Lijst om de verschillende variaties van de netlist op te slaan
    variations = []

    # Genereer het gewenste aantal variaties
    for _ in range(num_variations):
        # Kopieer de gesorteerde netlist om een nieuwe variatie te maken
        shuffled_netlist = sorted_netlist[:]
        
        # Zoek de indices van verbindingen met dezelfde frequentie
        i = 0
        while i < len(shuffled_netlist):
            current_freq = node_counts[shuffled_netlist[i][0]] + node_counts[shuffled_netlist[i][1]]
            # Zoek alle verbindingen met dezelfde frequentie
            same_freq_indices = [i]
            j = i + 1
            while j < len(shuffled_netlist) and (node_counts[shuffled_netlist[j][0]] + node_counts[shuffled_netlist[j][1]]) == current_freq:
                same_freq_indices.append(j)
                j += 1

            # Shuffle de verbindingen met dezelfde frequentie
            same_freq_connections = [shuffled_netlist[k] for k in same_freq_indices]
            random.shuffle(same_freq_connections)
            
            # Zet de shuffled verbindingen terug in de lijst
            for idx, new_idx in zip(same_freq_indices, range(len(same_freq_connections))):
                shuffled_netlist[idx] = same_freq_connections[new_idx]
            
            # Ga verder met de volgende groep
            i = j
        
        variations.append(shuffled_netlist)

    return variations

def sort_multiple_netlist_distance(netlist, nodeslist, num_variations = 100):
    """
    Genereer verschillende gesorteerde versies van de netlist, gebaseerd op de Manhattan-afstand
    tussen nodes voor elke verbinding. Als meerdere verbindingen dezelfde afstand hebben, worden
    ze willekeurig herschikt.

    Parameters:
    netlist (list of tuples): Een lijst van verbindingen, waarbij elke tuple twee nodes verbindt.
    nodeslist (list of Node): Een lijst van Node-objecten, waar elke node een x- en y-coördinaat heeft.
    num_variations (int): Het aantal gesorteerde versies van de netlist die gegenereerd moeten worden.

    Returns:
    list of lists of tuples: Een lijst van gesorteerde netlists.
    """
    # Bereken de Manhattan-afstand voor elke verbinding
    distances = {}
    for connection in netlist:
        x_1 = nodeslist[connection[0] - 1].give_x()
        y_1 = nodeslist[connection[0] - 1].give_y()
        x_2 = nodeslist[connection[1] - 1].give_x()
        y_2 = nodeslist[connection[1] - 1].give_y()

        dist = abs(x_1 - x_2) + abs(y_1 - y_2)
        distances[connection] = dist

    # Sorteer de netlist op basis van de afstand
    sorted_netlist = sorted(netlist, key=lambda x: distances[x], reverse=False)

    # Lijst om de verschillende variaties van de netlist op te slaan
    variations = []

    # Genereer het gewenste aantal variaties
    for _ in range(num_variations):
        # Kopieer de gesorteerde netlist om een nieuwe variatie te maken
        shuffled_netlist = sorted_netlist[:]
        
        # Zoek de indices van verbindingen met dezelfde afstand
        i = 0
        while i < len(shuffled_netlist):
            current_dist = distances[shuffled_netlist[i]]
            # Zoek alle verbindingen met dezelfde afstand
            same_dist_indices = [i]
            j = i + 1
            while j < len(shuffled_netlist) and distances[shuffled_netlist[j]] == current_dist:
                same_dist_indices.append(j)
                j += 1

            # Shuffle de verbindingen met dezelfde afstand
            same_dist_connections = [shuffled_netlist[k] for k in same_dist_indices]
            random.shuffle(same_dist_connections)
            
            # Zet de shuffled verbindingen terug in de lijst
            for idx, new_idx in zip(same_dist_indices, range(len(same_dist_connections))):
                shuffled_netlist[idx] = same_dist_connections[new_idx]
            
            # Ga verder met de volgende groep
            i = j
        
        variations.append(shuffled_netlist)

    return variations
