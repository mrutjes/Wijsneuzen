import pandas as pd
import matplotlib.pyplot as plt
from code.classes.nodes_class import Node
from code.classes.wire_class import Wire, WirePoint
from code.classes.grid_class import Grid_3D
import numpy as np

def manhattan_wire(node1: Node, node2: Node, grid: Grid_3D, nodes_csv_path: str, netlist_csv_path: str):
    """
    Creates a wire based on the Manhattan distance between node1 and node2.
    Ensures strictly Manhattan movement, with only one coordinate changing at a time.
    Avoids overlap with existing wires by dynamically rerouting and resolving conflicts.
    """


    wire = Wire(start_node=node1, end_node=node2, nodes_csv_path=nodes_csv_path, netlist_csv_path=netlist_csv_path)

    x_start, y_start = node1.give_x(), node1.give_y()
    x_end, y_end = node2.give_x(), node2.give_y()

    dict_count_nodes = wire.count_nodes_connections()

    sorted_dict_nodes_desc = dict(sorted(dict_count_nodes.items(), key=lambda item: item[1], reverse=True))
    netlist = wire.give_netlist()

    # BEGIN met een lege lijst
    ordered_netlist = []
    print(wire._nodes)

    for key, value in sorted_dict_nodes_desc.items():  # .items() niet vergeten!
        if value > 1:
            print(key, value)
            print(type(wire._nodes[key]))
            grid.add_reservation(WirePoint(wire._nodes[key].give_x(), wire._nodes[key].give_y(), wire._nodes[key].give_z()))
                                
        to_remove = []
        for i, conn in enumerate(netlist):
            # conn is bijvoorbeeld (startNode, endNode)
            if conn[0] == key:
                ordered_netlist.append((conn[0], conn[1]))
                to_remove.append(i)
            elif conn[1] == key:
                ordered_netlist.append((conn[1], conn[0]))
                to_remove.append(i)

        # Verwijder nu alle gebruikte items
        for i in sorted(to_remove, reverse=True):
            netlist.pop(i)

    print(ordered_netlist)




    x_curr, y_curr, z_curr = x_start, y_start, 0
    
    step = 0

    # Keep track of how many times we've tried fallback
    # to avoid an infinite loop scenario
    fallback_attempts = 0
    max_fallbacks = 500  # Arbitrary large limit

    while (x_curr, y_curr) != (x_end, y_end):

        # --------------------------------------------------
        # IF x_curr < x_end
        # --------------------------------------------------
        if x_curr < x_end:
            step = 1
            wire.add_wire_point(WirePoint(x_curr + step, y_curr, z_curr))
            x_curr += step

            if not grid.check_valid_addition(wire):
                # Fallback logic: pop, revert, try next direction
                wire.pop_wire_point()
                x_curr -= step
                fallback_attempts += 1
                if fallback_attempts > max_fallbacks:
                    raise ValueError("Too many fallback attempts – no valid path found.")
                
                # Try a Y or Z move (example: first y, if that fails, then z)
                if not try_next_direction(wire, grid, x_curr, y_curr, z_curr, x_end, y_end):
                    # If next direction also fails, pop once more and try something else
                    if wire.get_length() > 0:
                        wire.pop_wire_point()
                    # Optional: revert coordinate if needed
                    # ...
                    # If absolutely everything fails, raise an error
                    raise ValueError("No possible valid path from fallback in x < x_end.")
            else:
                # If valid addition, reset fallback attempts
                fallback_attempts = 0

        # --------------------------------------------------
        # ELIF x_curr > x_end
        # --------------------------------------------------
        elif x_curr > x_end:
            step = -1
            wire.add_wire_point(WirePoint(x_curr + step, y_curr, z_curr))
            x_curr += step

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                x_curr -= step
                fallback_attempts += 1
                if fallback_attempts > max_fallbacks:
                    raise ValueError("Too many fallback attempts – no valid path found.")

                # Try alternative directions
                if not try_next_direction(wire, grid, x_curr, y_curr, z_curr, x_end, y_end):
                    if wire.get_length() > 0:
                        wire.pop_wire_point()
                    raise ValueError("No possible valid path from fallback in x > x_end.")
            else:
                fallback_attempts = 0

        # --------------------------------------------------
        # ELIF y_curr < y_end
        # --------------------------------------------------
        elif y_curr < y_end:
            step = 1
            wire.add_wire_point(WirePoint(x_curr, y_curr + step, z_curr))
            y_curr += step

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                y_curr -= step
                fallback_attempts += 1
                if fallback_attempts > max_fallbacks:
                    raise ValueError("Too many fallback attempts – no valid path found.")

                if not try_next_direction(wire, grid, x_curr, y_curr, z_curr, x_end, y_end):
                    if wire.get_length() > 0:
                        wire.pop_wire_point()
                    raise ValueError("No possible valid path from fallback in y < y_end.")
            else:
                fallback_attempts = 0

        # --------------------------------------------------
        # ELIF y_curr > y_end
        # --------------------------------------------------
        elif y_curr > y_end:
            step = -1
            wire.add_wire_point(WirePoint(x_curr, y_curr + step, z_curr))
            y_curr += step

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                y_curr -= step
                fallback_attempts += 1
                if fallback_attempts > max_fallbacks:
                    raise ValueError("Too many fallback attempts – no valid path found.")

                if not try_next_direction(wire, grid, x_curr, y_curr, z_curr, x_end, y_end):
                    if wire.get_length() > 0:
                        wire.pop_wire_point()
                    raise ValueError("No possible valid path from fallback in y > y_end.")
            else:
                fallback_attempts = 0

        # --------------------------------------------------
        # ELIF z_curr > 0
        # --------------------------------------------------
        elif z_curr > 0:
            step = -1
            wire.add_wire_point(WirePoint(x_curr, y_curr, z_curr + step))
            z_curr += step

            if not grid.check_valid_addition(wire):
                wire.pop_wire_point()
                z_curr -= step
                fallback_attempts += 1
                if fallback_attempts > max_fallbacks:
                    raise ValueError("Too many fallback attempts – no valid path found.")

                if not try_next_direction(wire, grid, x_curr, y_curr, z_curr, x_end, y_end):
                    if wire.get_length() > 0:
                        wire.pop_wire_point()
                    raise ValueError("No possible valid path from fallback in z_curr > 0.")
            else:
                fallback_attempts = 0

        else:
            # If none of the if/elif conditions match, we are stuck
            fallback_attempts += 1
            if fallback_attempts > max_fallbacks:
                raise ValueError("Too many fallback attempts – no valid path found.")

            # Pop one or two points, revert to a known good state, try something else
            if wire.get_length() > 0:
                wire.pop_wire_point()
            if wire.get_length() > 0:
                wire.pop_wire_point()

            # Possibly revert coordinates
            # ...
            # Then continue, hoping to find an alternate route
            continue

    return wire


def try_next_direction(wire, grid, x_curr, y_curr, z_curr, x_end, y_end):
    """
    Attempt one or more alternative directions when the current step fails.
    Returns True if a valid path was added, False otherwise.
    
    This is just a placeholder. In practice, you'd replicate the fallback logic
    from your main loop, but try different coordinate changes (like y first,
    then z, etc.).
    """
    # Example: Try step in y if y_curr < y_end
    if y_curr < y_end:
        step = 1
        wire.add_wire_point(WirePoint(x_curr, y_curr + step, z_curr))
        if grid.check_valid_addition(wire):
            return True
        else:
            wire.pop_wire_point()

    # Then maybe try z, etc. This is just a skeleton:
    if z_curr == 0:
        # Suppose we can go up in z
        step = 1
        wire.add_wire_point(WirePoint(x_curr, y_curr, z_curr + step))
        if grid.check_valid_addition(wire):
            return True
        else:
            wire.pop_wire_point()

    # If all attempts fail:
    return False
