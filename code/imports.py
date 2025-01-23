import pandas as pd
from code.classes.nodes_class import Node
import math
import random
import itertools

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
    Generate a random sample of `num_samples` permutations from the netlist.
    """
    total_permutations = math.factorial(len(netlist))
    
    if num_samples >= total_permutations:
        return list(itertools.permutations(netlist))
    
    selected_permutations = set()
    while len(selected_permutations) < num_samples:
        perm = tuple(random.sample(netlist, len(netlist)))
        selected_permutations.add(perm)

    return list(selected_permutations)