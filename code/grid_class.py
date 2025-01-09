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
        self.punt_dict = {
            (x, y, z): 0
            for x in range(self.n) for y in range(self.m) for z in range(self.hoogte)
        }
        self.aantal_lijnen = 0

    def plaats_wire(self, wire):
        """
        Plaatst een wire in de grid en telt hoeveel keer elk punt wordt doorkruist.

        :param wire: Een lijst van tuples met coördinaten [(x1, y1, z1), (x2, y2, z2), ...].
        """
        for x, y, z in wire:
            if 0 <= x < self.n and 0 <= y < self.m and 0 <= z < self.hoogte:
                self.punt_dict[(x, y, z)] += 1
            else:
                raise IndexError("Coördinaten buiten de grid.")
        self.aantal_lijnen += len(wire) - 1

    def tel_lijnen_punt(self):
        """
        Retourneert de dictionary met het aantal lijnen per punt in de grid.
        """
        return self.punt_dict

    def totaal_kruisingen(self):
        """
        Berekent het totale aantal kruisingen in de hele grid.
        """
        kruisingen = 0
        for waarde in self.punt_dict.values():
            if waarde > 1:
                kruisingen += waarde - 1
        return kruisingen

    def kosten(self):
        """
        Berekent de kosten op basis van:
        - Kruisingen: elke kruising kost 300
        - Aantal lijnen: elke lijn kost 1
        """
        kruisingen = self.totaal_kruisingen()
        return kruisingen * 300 + self.aantal_lijnen

