import pandas as pd

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def importeer_nodes(self, csv_path):
        data = pd.read_csv(csv_path)
        nodes = []

        for _, row in data.iterrows():
            node = Node(row['x'], row['y'])
            nodes.append(node)

        return nodes


node_instance = Node(0, 0)
nodes = node_instance.importeer_nodes("nodes.csv")
