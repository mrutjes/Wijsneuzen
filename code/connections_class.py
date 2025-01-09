import pandas as pd

def importeer_netlist(csv_path):
    """
    Maakt een lijst van tuples (int, int) die de indices van te verbinden gates voorstelt.
    """
    data = pd.read_csv(csv_path)
    return [
        (int(row['chip_a']), int(row['chip_b']))
        for _, row in data.iterrows()
    ]
