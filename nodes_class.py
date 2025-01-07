import pandas as pd

class Node:
    def __init__(self, x, y):
        """
        Initialiseer een node op de base layer van het grid.

        :param x: De x-coördinaat van de node.
        :param y: De y-coördinaat van de node.
        """
        self.x = x
        self.y = y

    # Functie om nodes te importeren vanuit een CSV-bestand
    def importeer_nodes(csv_path):
        data = pd.read_csv(csv_path)
        nodes = {}

        for row in data.iterrows():
            node = Node(row['x'], row['y'])
            nodes.add(node)

        return nodes
