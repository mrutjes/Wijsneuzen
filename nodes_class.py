import pandas as pd
import os

class Node:
    def __init__(self, x, y):
        """
        Initialiseer een node op de base layer van het grid.

        :param x: De x-coördinaat van de node.
        :param y: De y-coördinaat van de node.
        """
        self.x = x
        self.y = y
        self.nodes = set()

def importeer_netlist(csv_path):
    """Maakt een tuple set van alle nodes die in een netlist gegeven staan"""
    data = pd.read_csv(csv_path)
    return {
        (int(row['chip_a']), int(row['chip_b']))
        for _, row in data.iterrows()
    }

# Test run
node_set = importeer_netlist('../gates&netlists/chip_0/netlist_1.csv')
print(node_set)

