from code.algorithms import a_star_algorithm, dfs_algorithm, lee_algorithm, manhattan_wire
import itertools
import math
import random
random.seed(43)

# Sorteer functies

def random_permutations(netlist, num_samples):
    """
    Generate a random sample of ⁠ num_samples ⁠ permutations from the netlist.
    """
    total_permutations = math.factorial(len(netlist))
    
    if num_samples >= total_permutations:
        return list(itertools.permutations(netlist))
    
    selected_permutations = set()
    while len(selected_permutations) < num_samples:
        perm = tuple(random.sample(netlist, len(netlist)))
        selected_permutations.add(perm)

    return list(selected_permutations)

def sort_netlist_busy_nodes(netlist):
    """
    Sorts a netlist based on how many times each node occurs in the netlist.
    
    Parameters:
    netlist (list of tuples): A list where each tuple represents a connection 
                              (e.g., [(node1, node2), (node2, node3), ...]).
    
    Returns:
    list of tuples: A sorted netlist where the nodes with the highest occurrences appear first.
    """
    node_counts = {}
    for connection in netlist:
        for node in connection:
            if node in node_counts:
                node_counts[node] += 1
            else:
                node_counts[node] = 1

    sorted_netlist = sorted(netlist, key=lambda x: (node_counts[x[0]] + node_counts[x[1]]), reverse=True)

    return sorted_netlist

def sort_netlist_distance(netlist, nodeslist):
    """
    Sorts a netlist based on the distance between two nodes for each connection.
    """
    num = 0
    dict = {}

    for connection in netlist:
        num += 1
        x_1 = nodeslist[connection[0] - 1].give_x()
        y_1 = nodeslist[connection[0] - 1].give_y()
        x_2 = nodeslist[connection[1] - 1].give_x()
        y_2 = nodeslist[connection[1] - 1].give_y()

        dist = abs(x_1 - x_2) + abs(y_1 - y_2)

        dict[(connection)] = dist

    sorted_netlist = sorted(netlist, key=lambda x: (dict[x]), reverse=False)

    return sorted_netlist

def sort_multiple_netlist_busy_nodes(netlist, num_variations = 100):
    """
    Genereer verschillende gesorteerde versies van de netlist, gebaseerd op de frequentie van nodes.
    Als meerdere verbindingen dezelfde frequentie hebben, worden ze willekeurig herschikt.

    Parameters:
    netlist (list of tuples): Een lijst van verbindingen, waarbij elke tuple twee nodes verbindt.
    num_variations (int): Aantal gesorteerde versies van de netlist die gegenereerd moeten worden.

    Returns:
    list of lists of tuples: Een lijst van gesorteerde netlists.
    """
    # Tel hoe vaak elke node voorkomt in de netlist
    node_counts = {}
    for connection in netlist:
        for node in connection:
            node_counts[node] = node_counts.get(node, 0) + 1

    # Sorteer de netlist op basis van de frequentie van de nodes
    sorted_netlist = sorted(netlist, key=lambda x: (node_counts[x[0]] + node_counts[x[1]]), reverse=True)

    # Lijst om de verschillende variaties van de netlist op te slaan
    variations = []

    # Genereer het gewenste aantal variaties
    for _ in range(num_variations):
        # Kopieer de gesorteerde netlist om een nieuwe variatie te maken
        shuffled_netlist = sorted_netlist[:]
        
        # Zoek de indices van verbindingen met dezelfde frequentie
        i = 0
        while i < len(shuffled_netlist):
            current_freq = node_counts[shuffled_netlist[i][0]] + node_counts[shuffled_netlist[i][1]]
            # Zoek alle verbindingen met dezelfde frequentie
            same_freq_indices = [i]
            j = i + 1
            while j < len(shuffled_netlist) and (node_counts[shuffled_netlist[j][0]] + node_counts[shuffled_netlist[j][1]]) == current_freq:
                same_freq_indices.append(j)
                j += 1

            # Shuffle de verbindingen met dezelfde frequentie
            same_freq_connections = [shuffled_netlist[k] for k in same_freq_indices]
            random.shuffle(same_freq_connections)
            
            # Zet de shuffled verbindingen terug in de lijst
            for idx, new_idx in zip(same_freq_indices, range(len(same_freq_connections))):
                shuffled_netlist[idx] = same_freq_connections[new_idx]
            
            # Ga verder met de volgende groep
            i = j
        
        variations.append(shuffled_netlist)

    return variations

def sort_multiple_netlist_distance(netlist, nodeslist, num_variations = 100):
    """
    Genereer verschillende gesorteerde versies van de netlist, gebaseerd op de Manhattan-afstand
    tussen nodes voor elke verbinding. Als meerdere verbindingen dezelfde afstand hebben, worden
    ze willekeurig herschikt.

    Parameters:
    netlist (list of tuples): Een lijst van verbindingen, waarbij elke tuple twee nodes verbindt.
    nodeslist (list of Node): Een lijst van Node-objecten, waar elke node een x- en y-coördinaat heeft.
    num_variations (int): Het aantal gesorteerde versies van de netlist die gegenereerd moeten worden.

    Returns:
    list of lists of tuples: Een lijst van gesorteerde netlists.
    """
    # Bereken de Manhattan-afstand voor elke verbinding
    distances = {}
    for connection in netlist:
        x_1 = nodeslist[connection[0] - 1].give_x()
        y_1 = nodeslist[connection[0] - 1].give_y()
        x_2 = nodeslist[connection[1] - 1].give_x()
        y_2 = nodeslist[connection[1] - 1].give_y()

        dist = abs(x_1 - x_2) + abs(y_1 - y_2)
        distances[connection] = dist

    # Sorteer de netlist op basis van de afstand
    sorted_netlist = sorted(netlist, key=lambda x: distances[x], reverse=False)

    # Lijst om de verschillende variaties van de netlist op te slaan
    variations = []

    # Genereer het gewenste aantal variaties
    for _ in range(num_variations):
        # Kopieer de gesorteerde netlist om een nieuwe variatie te maken
        shuffled_netlist = sorted_netlist[:]
        
        # Zoek de indices van verbindingen met dezelfde afstand
        i = 0
        while i < len(shuffled_netlist):
            current_dist = distances[shuffled_netlist[i]]
            # Zoek alle verbindingen met dezelfde afstand
            same_dist_indices = [i]
            j = i + 1
            while j < len(shuffled_netlist) and distances[shuffled_netlist[j]] == current_dist:
                same_dist_indices.append(j)
                j += 1

            # Shuffle de verbindingen met dezelfde afstand
            same_dist_connections = [shuffled_netlist[k] for k in same_dist_indices]
            random.shuffle(same_dist_connections)
            
            # Zet de shuffled verbindingen terug in de lijst
            for idx, new_idx in zip(same_dist_indices, range(len(same_dist_connections))):
                shuffled_netlist[idx] = same_dist_connections[new_idx]
            
            # Ga verder met de volgende groep
            i = j
        
        variations.append(shuffled_netlist)

    return variations

# Sorteer functies: Q Learning

alpha = 0.1
gamma = 0.9
epsilon = 0.2
q_table = {}

def state_to_tuple(state):
    """
    Zet de netlist om naar een hashbare tuple voor de Q-table.
    """
    return tuple(state)

def choose_action(state, netlist):
    """
    Kies een actie (wissel twee items in de netlist) op basis van epsilon-greedy policy.
    """
    if random.uniform(0, 1) < epsilon:
        i, j = random.sample(range(len(netlist)), 2)
    else:
        possible_actions = [(s, a) for (s, a) in q_table if s == state]
        if not possible_actions:
            i, j = random.sample(range(len(netlist)), 2)
        else:
            _, best_action = max(possible_actions, key=lambda x: q_table[x])
            i, j = best_action

    return i, j

def update_q_table(state, action, reward, next_state):
    """
    Update de Q-table volgens de Q-learning formule.
    """
    key = (state, action)
    next_state_keys = [(next_state, a) for a in range(len(next_state))]
    
    next_max = max((q_table[k] for k in next_state_keys if k in q_table), default=0)

    q_table[key] = q_table.get(key, 0) + alpha * (reward + gamma * next_max - q_table.get(key, 0))

# Setup functies

def get_netlist():
    while True:
        netlist = input("What netlist do you want to use? Answer must lie between 1-9: ").lower()
        if netlist == '1' or netlist == '2' or netlist == '3':
            chip = '0'
            break
        elif netlist == '4' or netlist == '5' or netlist == '6':
            chip = '1'
            break
        elif netlist == '7' or netlist == '8' or netlist == '9':
            chip = '2'
            break
        else:
            print("Not a valid entry")
    return chip, netlist

def get_algorithms():
    while True:
        algorithm = input("What algorithm do you want to use? Choose between Manhattan (M), Depth First (D), Lee (L) or A* (A): ").lower()
        if algorithm == 'm' or algorithm == 'manhattan':
            functie = manhattan_wire
            break
        elif algorithm == 'd' or algorithm == 'depth first':
            functie = dfs_algorithm
            break
        elif algorithm == 'l' or algorithm == 'lee':
            functie = lee_algorithm
            break
        elif algorithm == 'a' or algorithm == 'a*':
            functie = a_star_algorithm
            break
        else:
            print("Not a valid entry")
    return functie, algorithm

def get_sorting_method(netlist, nodes_list, iter):
    if iter == 1:
        while True:
            ans = input("How do you want to sort the netlist? Choose between by: Random (R), Busy nodes (B) or Distance of a connection (D): ").lower()
            if ans == 'r' or ans == 'random':
                sort = random_permutations(netlist, int(iter))
                break
            elif ans == 'd' or ans == 'distance of a connection':
                sort = sort_netlist_distance(netlist, nodes_list)
                break
            elif ans == 'b' or ans == 'busy nodes':
                sort = sort_netlist_busy_nodes(netlist)
                break
            else:
                print("Not a valid entry")
    else:
        while True:
            ans = input("How do you want to sort the netlist? Choose between by: Random (R), Q-Learning (Q), Busy nodes (B) or Distance of a connection (D): ").lower()
            if ans == 'r' or ans == 'random':
                sort = random_permutations(netlist, int(iter))
                break
            elif ans == 'd' or ans == 'distance of a connection':
                sort = sort_multiple_netlist_distance(netlist, nodes_list, int(iter))
                break
            elif ans == 'b' or ans == 'busy nodes':
                sort = sort_multiple_netlist_busy_nodes(netlist, int(iter))
                break
            elif ans == 'q' or ans == 'q-learning' or ans == 'q learning':
                sort = 'q'
                break
            else:
                print("Not a valid entry")
    return sort

def get_singular_multiple():
    while True:
        try:
            runs = int(input("How many times do you want to run the algorithm? "))
            if runs <= 0:
                print("Please enter a positive number.")
            elif runs >= 1:
                return runs
        except ValueError:
            print("Not a valid entry. Please enter a number.")