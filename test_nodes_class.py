import unittest
import pandas as pd
from io import StringIO
from nodes_class import Node  

class TestNode(unittest.TestCase):

    def setUp(self):
        """
        Stel testdata en een Node-instantie in.
        """
        self.node_instance = Node(0, 0)

        # Maak een mock CSV-bestand als testdata
        self.csv_data = StringIO("""x,y
1,2
3,4
5,6
""")
        self.expected_nodes = [
            (1, 2),
            (3, 4),
            (5, 6)
        ]

    def test_importeer_nodes_correct_data(self):
        """
        Test of nodes correct worden geïmporteerd uit een CSV-bestand.
        """
        # Lees de mock CSV-data in als een Pandas DataFrame
        data = pd.read_csv(self.csv_data)
        data.to_csv("mock_nodes.csv", index=False)  # Maak een tijdelijk CSV-bestand

        # Importeer de nodes
        nodes = self.node_instance.importeer_nodes("mock_nodes.csv")

        # Controleer dat het aantal nodes klopt
        self.assertEqual(len(nodes), len(self.expected_nodes))

        # Controleer dat de nodes correct zijn gemaakt
        for node, (x, y) in zip(nodes, self.expected_nodes):
            self.assertEqual(node.x, x)
            self.assertEqual(node.y, y)

    def test_importeer_nodes_empty_file(self):
        """
        Test het importeren van een leeg CSV-bestand.
        """
        empty_csv = StringIO("x,y\n")
        data = pd.read_csv(empty_csv)
        data.to_csv("mock_empty_nodes.csv", index=False)

        # Importeer de nodes
        nodes = self.node_instance.importeer_nodes("mock_empty_nodes.csv")

        # Controleer dat de lijst leeg is
        self.assertEqual(len(nodes), 0)

    def test_importeer_nodes_missing_columns(self):
        """
        Test het importeren van een CSV zonder de kolommen 'x' en 'y'.
        """
        invalid_csv = StringIO("a,b\n1,2\n3,4\n")
        data = pd.read_csv(invalid_csv)
        data.to_csv("mock_invalid_nodes.csv", index=False)

        # Controleer of een fout wordt opgegooid
        with self.assertRaises(KeyError):
            self.node_instance.importeer_nodes("mock_invalid_nodes.csv")

    def tearDown(self):
        """
        Ruim bestanden of andere resources op.
        """
        import os
        if os.path.exists("mock_nodes.csv"):
            os.remove("mock_nodes.csv")
        if os.path.exists("mock_empty_nodes.csv"):
            os.remove("mock_empty_nodes.csv")
        if os.path.exists("mock_invalid_nodes.csv"):
            os.remove("mock_invalid_nodes.csv")

if __name__ == "__main__":
    unittest.main()
