from string import ascii_uppercase
from const import EMPTY, SHIP, HIT, MISS, SUNK, SEPERATOR
from const import Point


class Board:
    def __init__(self, size):

        self.size = size
        self.ships = {}
        self.guesses = []
        self.hits = 0

    def is_on_board(self, position):
        for coordinate in position:
            if not (0 <= coordinate < self.size):
                return False
        return True

    def is_ship_on_board(self, ship):

        row, column = ship.position

        if ship.orientation == "H":
            long, short = column, row
        elif ship.orientation == "V":
            long, short = row, column

        if short > self.size:
            return False

        if long + ship.length > self.size:
            return False

        for direction in ship.position:
            if direction < 0:
                return False

        return True

    @staticmethod
    def generate_ship(ship):

        row, column = ship.position

        ship_positions = []
        for i in range(ship.length):
            if ship.orientation == "H":
                ship_positions.append(Point(row, column + i))
            elif ship.orientation == "V":
                ship_positions.append(Point(row + i, column))

        return ship_positions

    def check_ship_collisions(self, ship):

        for other_ship in self.ships:
            other_ship_set = set(self.generate_ship(other_ship))
            current_ship_set = set(self.generate_ship(ship))
            if not other_ship_set.isdisjoint(current_ship_set):
                return True
        return False

    def place_ship(self, ship):
        self.ships[ship] = ship.length

    def delete_ship(self, ship):
        del self.ships[ship]

    def is_guessed(self, position):

        return position in self.guesses

    def guess_position(self, position):

        self.guesses.append(position)

        for ship in self.ships:
            if position in self.generate_ship(ship):
                self.ships[ship] -= 1
                if self.ships[ship] == 0:
                    result = SUNK
                else:
                    result = HIT
                self.hits += 1
                break
        else:
            result = MISS

        return result

    def print_rows(self, show_ships=True):

        seperator_length = len(SEPERATOR) + 1
        column_headers = "".join(
            [str(i).ljust(seperator_length) for i in range(1, self.size + 1)]
        )

        yield "   " + column_headers

        for row in range(self.size):
            row_letter = ascii_uppercase[row]

            row_text = ""
            for column in range(self.size):
                current_position = Point(row, column)

                for ship in self.ships:
                    if current_position in self.generate_ship(ship):
                        if current_position in self.guesses:
                            value = HIT
                        else:
                            if show_ships:
                                value = SHIP
                            else:
                                value = EMPTY
                        break
                else:
                    if current_position in self.guesses:
                        value = MISS
                    else:
                        value = EMPTY
                row_text += value + SEPERATOR

            yield row_letter + "  " + row_text

    def display(self, show_ships=True):

        for row in self.print_rows(show_ships):
            print(row)

    def all_ships_sunk(self):

        for ship_health in self.ships.values():
            if ship_health > 0:
                return False
        return True

    @staticmethod
    def convert_position(position):
        row = position[0]
        column = position[1:]

        row_number = ascii_uppercase.index(row)
        column_number = int(column) - 1

        return Point(row_number, column_number)
