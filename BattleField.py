from random import randint, choice


class BattleField:
    def __init__(self):
        self.ships = [(4, 1), (3, 2), (2, 3), (1, 4)]
        self.ships_on_field = []

    def place_ships(self):
        self.ships_on_field = []
        direction = ['row', 'column']
        for ship_type in range(len(self.ships)):
            for ship in range(self.ships[ship_type][1]):
                ship_coordinates = []
                last_coordinate = None
                ship_direction = None
                i = 0
                while i < self.ships[ship_type][0]:
                    if not last_coordinate:
                        coordinate = (randint(0, 9), randint(0, 9))
                        if self._is_valid_place(coordinate):
                            ship_coordinates.append(coordinate)
                            last_coordinate = coordinate
                            ship_direction = choice(direction)
                            i += 1
                    else:
                        if ship_direction == 'row':
                            coordinate = (last_coordinate[0], last_coordinate[1] + 1)
                            if self._is_valid_place(coordinate):
                                ship_coordinates.append(coordinate)
                                last_coordinate = coordinate
                                i += 1
                            else:
                                i = 0
                                ship_coordinates = []
                                last_coordinate = None
                                ship_direction = None
                        else:
                            coordinate = (last_coordinate[0] + 1, last_coordinate[1])
                            if self._is_valid_place(coordinate):
                                ship_coordinates.append(coordinate)
                                last_coordinate = coordinate
                                i += 1
                            else:
                                i = 0
                                ship_coordinates = []
                                last_coordinate = None
                                ship_direction = None
                self.ships_on_field.append(ship_coordinates)

    def _is_valid_place(self, coordinate):
        if coordinate[0] > 9 or coordinate[1] > 9:
            return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                busy_cells = []
                for k in self.ships_on_field:
                    for l in k:
                        busy_cells.append(l)
                if (coordinate[0] + i, coordinate[1] + j) in busy_cells:
                    return False
        return True

    def get_ships(self):
        return self.ships_on_field
