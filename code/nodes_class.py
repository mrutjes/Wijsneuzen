import pandas as pd

class Node:
    """
    Class for nodes in the grid.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0


    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.x, self.y) == (other.x, other.y)
    

    def __str__(self):
        return f'({self.x}, {self.y})'
    

def import_nodes(csv_path) -> list[Node]:
    """
    Imports nodes based on a csv file and returns a list of Node objects.
    """
    data = pd.read_csv(csv_path)

    return [
        Node(int(row['x']), int(row['y']))
        for _, row in data.iterrows()
    ]
