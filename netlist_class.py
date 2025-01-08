import pandas as pd

class NetList:
    
    def __init__(self):
        self.nodes_connections = set()

    def importeer_nodes(self, csv_path):
        data = pd.read_csv(csv_path)

        for _, row in data.iterrows():
            chip_a = row['chip_a']
            chip_b = row['chip_b']

            if isinstance(chip_a, int) and isinstance(chip_b, int):
                self.nodes_connections.add((chip_a, chip_b))

    
