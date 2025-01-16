class Node:
    """
    Class for nodes in the grid.
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._z = 0


    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self._x, self._y) == (other._x, other._y)
    

    def __str__(self):
        return f'({self._x}, {self._y})'
    

    def give_x(self):
        return self._x
    

    def give_y(self):
        return self._y
    
    
    def give_z(self):
        return 0
    
    

