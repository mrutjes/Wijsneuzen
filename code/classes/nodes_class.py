class Node:
    """
    Class for nodes in the grid.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0


    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.x, self.y) == (other.x, other.y)
    

    def __str__(self):
        return f'({self.x}, {self.y})'
    

