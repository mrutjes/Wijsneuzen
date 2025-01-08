#test

class Grid_3D:
    def __init__(self, n, m):
        """

        Maakt een grid van n x m x 8.
        n = x dimensie
        m = y dimensie

        """
        self.n = n
        self.m = m
        self.hoogte = 8
        # maak de grid met nullen
        self.grid = [[[0 for z in range(self.hoogte)] for y in range(self.m)] for x in range(self.n)]

    def plaats_node(self, node, z=0):
        """
        Plaatst een node op de gegeven x, y en z-coördinaat.

        :param node: Een BaseLayerNode-object.
        :param z: De hoogte waarop de node wordt geplaatst (standaard 0).
        """
        if 0 <= node.x < self.n and 0 <= node.y < self.m and 0 <= z < self.hoogte:
            self.grid[node.x][node.y][z] = node
        else:
            raise IndexError("Coördinaten buiten het grid.")
    
    def plaats_wire(self, wire):
        pass

    def haal_waarde(self, x, y, z):
        """
        Haalt de waarde op van een specifieke locatie in het grid.

        :param x: X-coördinaat.
        :param y: Y-coördinaat.
        :param z: Z-coördinaat (hoogte).
        :return: De waarde op de gegeven locatie.
        """
        if 0 <= x < self.n and 0 <= y < self.m and 0 <= z < self.hoogte:
            return self.grid[x][y][z]
        else:
            raise IndexError("Coördinaten buiten het grid.")

# Voorbeeld van gebruik:
grid = Grid_3D(4, 5)  # Maak een 4x5x8 grid

print(grid.haal_waarde(1, 1, 2))
