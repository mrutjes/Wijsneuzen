import pandas as pd

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        self.nodes = []

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.x, self.y) == (other.x, other.y)
    
    def __str__(self):
        return f'({self.x}, {self.y})'
    
def importeer_nodes(csv_path):
    """Importeert de nodes als Node-objecten in een lijst."""
    data = pd.read_csv(csv_path)
    return [
        Node(int(row['x']), int(row['y']))
        for _, row in data.iterrows()
    ]
