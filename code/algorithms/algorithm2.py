import pandas as pd
import matplotlib.pyplot as plt
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
import numpy as np

#def algorithm2(netlist: str):


if __name__ == '__main__':
    nodes_csv_path = './gates&netlists/chip_0/print_0.csv'
    netlist_csv_path = './gates&netlists/chip_0/netlist_1.csv'

    grid = Grid_3D(grid_width, grid_length, nodes_csv_path)

    nodes_list = import_nodes(nodes_csv_path)
    for node in nodes_list:
        grid.place_node(node)

    netlist = import_netlist(netlist_csv_path)
    node_count_dict = {}
    for connection in netlist:
        if connection[0] in node_count_dict:
            node_count_dict[connection[0]] += 1
        else:
            node_count_dict[connection[0]] = 1

        if connection[1] in node_count_dict:
            node_count_dict[connection[1]] += 1
        else:
            node_count_dict[connection[1]] = 1

    print(node_count_dict)



# Stap 1: Sorteer nodes

    1.1 Voor alle nodes in de netlist, noteer hoe vaak ze voorkomen.
    
    1.2 Voor alle connecties in de netlist, noteer de manhattan afstand.
    
    1.3 Sorteer netlist van nodes die vaak voorkomen naar nodes niet niet vaak voorkomen, daarna op afstand van klein naar groot.

# Stap 2: Voor elke connectie (start_node, eind_node) in de netlist:
    
    2.1 Maak een nieuwe Wire instantie met start_node en eind_node op z = 0

    2.2 Zolang de draad het eindpunt niet heeft bereikt:
        2.2.1 Bereken het verschil in x- en y-coördinaten:
            - Bereken tussen het huidige WirePoint en het eindpunt
            - Neem de stapgrootte:
                - stapgrootte = 1 als verschil positief is
                - stapgrootte = -1 als verschil negatief is
                
        2.2.2 Zet een stap:
            - Als het verschil in x groter of gelijk is dan in y:
                - Verander de x-coordinaat met + stapgrootte
                - Markeer x_positief = 1 als stapgrootte = 1, anders markeer x_negatief = 1 
                
            - Als het verschil in y groter is dan in x:
                - Verander de y-coordinaat met + stapgrootte
                - Markeer y_positief = 1 als stapgrootte = 1, anders markeer y_negatief = 1 

        2.2.3 WirePoint maken:
            - Maak een nieuw WirePoint met de nieuwe coördinaten
            - Voeg het WirePoint toe aan de draad met add_wire_point()

        2.2.4 Zolang check_valid_addition() voor het nieuwe WirePoint False retourneert:
            - Verwijder de WirePoint van de draad
            
            - Als de positieve x richting gemarkeerd is als geprobeerd:
                - Verander het y-coordinaat met + stapgrootte
                - Markeer y_positief = 1 als stapgrootte = 1, anders markeer y_negatief = 1
                
            - Anders, als de positieve y richting gemarkeerd is als geprobeerd:
                - Verander het x-coordinaat met - stapgrootte
                - Markeer x_positief = 1 als stapgrootte = -1, anders markeer x_negatief = 1
                
            - Anders, als de negatieve x richting gemarkeerd is als geprobeerd:
                - Verander het y-coordinaat met - stapgrootte
                - Markeer y_positief = 1 als stapgrootte = -1, anders markeer y_negatief = 1
                
            - Anders, als alle x en y richtingen gemarkeerd zijn als 1:
                - Verander het z-coordinaat met + 1
                - Markeer z_positief = 1
                
            - Anders, als z != 0 en z_negatief != 1:
                - Verander het z-coordinaat met - 1
                - Markeer z_negatief = 1
                
            - Anders, als alle richtingen gemarkeerd zijn als geprobeerd EN we zijn in de startnode:
                - Raise error "Node ingebouwd, kan draad niet leggen."
                
            - Anders:
                - Markeer x_positief = 1
                - Continue
                 
    2.3 Draad afmaken
        - Voeg de draad toe aan de grid met add_wire_list()
        - Voeg de draad toe aan de WirePoint dictionary in het grid met add_wire_dict()
        - Markeer x_postief, x_negatief, y_postief, y_negatief, z_postief, z_negatief = 0
            
# Stap 3: Bereken kosten
    
    3.1 Bereken de hoeveelheid kruispunten o.b.v. de dictionary
    
    3.2 Bereken de hoeveelheid draden
    
    3.3 Bereken de kosten
    
# Stap 4: Print de grid met draden