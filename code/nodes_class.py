import pandas as pd
import os

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nodes = []

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __str__(self):
        return f'({self.x}, {self.y})'
    
def importeer_nodes(csv_path):
    """Importeerd de nodes als Node in een lijst."""
    data = pd.read_csv(csv_path)
    return [
        (Node(int(row['x']), int(row['y'])))
        for _, row in data.iterrows()
    ]

#TODO
"""De netlist bestaat nu alleen nog uit integers, ervoor zorgen dat die ints een node vertegenwoordigen, zodat hij denkt dat Node 1 samen met Node 2 is verbonden."""
