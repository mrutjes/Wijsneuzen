import pandas as pd

def import_netlist(csv_path) -> list[tuple[int, int]]:
    """
    Generates a list of tuples from the netlist csv file.
    """
    data = pd.read_csv(csv_path)
    return [
        (int(row['chip_a']), int(row['chip_b']))
        for _, row in data.iterrows()
    ]
