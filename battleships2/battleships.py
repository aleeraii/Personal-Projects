from itertools import cycle
from collections import namedtuple
from string import ascii_uppercase

board_division = "  |  "
starter = ">"
ship_count = [5, 4, 3, 2, 1]
Point = namedtuple("Point", "x y")
Ship = namedtuple("Ship", "position length orientation")
size_of_board = 10
length_of_line = (size_of_board * 3) + 3
empty_field = "-"
ship_mark = "S"
hitted_place = "*"
missed_place = "M"
SUNK = "Sunk"
separator = "  "


class Board:
    def __init__(self, size):

        self.size = size
        self.ships = {}
        self.guesses = []
        self.hits = 0

    def on_board(self, position):
        for coordinate in position:
            if not (0 <= coordinate < self.size):
                return False
        return True

    def ship_in_board(self, ship):

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
    def make_ship(ship):

        row, column = ship.position

        ship_positions = []
        for i in range(ship.length):
            if ship.orientation == "H":
                ship_positions.append(Point(row, column + i))
            elif ship.orientation == "V":
                ship_positions.append(Point(row + i, column))

        return ship_positions

    def collision_check(self, ship):

        for other_ship in self.ships:
            other_ship_set = set(self.make_ship(other_ship))
            current_ship_set = set(self.make_ship(ship))
            if not other_ship_set.isdisjoint(current_ship_set):
                return True
        return False

    def place_equipment(self, ship):
        self.ships[ship] = ship.length

    def delete_equipment(self, ship):
        del self.ships[ship]

    def guessed(self, position):

        return position in self.guesses

    def guess_position(self, position):

        self.guesses.append(position)

        for ship in self.ships:
            if position in self.make_ship(ship):
                self.ships[ship] -= 1
                if self.ships[ship] == 0:
                    result = SUNK
                else:
                    result = hitted_place
                self.hits += 1
                break
        else:
            result = missed_place

        return result

    def print_rows(self, show_ships=True):

        seperator_length = len(separator) + 1
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
                    if current_position in self.make_ship(ship):
                        if current_position in self.guesses:
                            value = hitted_place
                        else:
                            if show_ships:
                                value = ship_mark
                            else:
                                value = empty_field
                        break
                else:
                    if current_position in self.guesses:
                        value = missed_place
                    else:
                        value = empty_field
                row_text += value + separator

            yield row_letter + "  " + row_text

    def display(self, show_ships=True):

        for row in self.print_rows(show_ships):
            print(row)

    def every_ship_sunked(self):

        for ship_health in self.ships.values():
            if ship_health > 0:
                return False
        return True

    @staticmethod
    def echange_pos_var(position):
        row = position[0]
        column = position[1:]

        row_number = ascii_uppercase.index(row)
        column_number = int(column) - 1

        return Point(row_number, column_number)


def clear_screen():

    print("\n" * 100)


def center(text, width=length_of_line):

    length = len(text)
    start = (width - length) // 2
    end = width - length - start
    output = (" " * start) + text + (" " * end)
    return output


class Game:
    def __init__(self):

        # Set up the variables
        self.players = "AB"
        self.player_names = {}
        self.boards = {player: Board(size_of_board) for player in self.players}
        self.ships = ship_count
        self.start()

        for player in self.players:
            self.set_up_boards(player)
        # Play the game
        for player in cycle(self.players):
            if self.turn(player):
                break

        winning_player = self.player_names[player]
        print(winning_player + " Won ")
        other_player = self.players.replace(player, "")
        with open("score.txt", 'a') as f:
            f.write(winning_player+"-"+str(self.boards[other_player].hits)+"\n")
        self.play_again()
        
    def play_again(self):
        val = input("Do you want to play again ? (y/n)")
        if val.lower() == "y":
            Game()
        elif val.lower() == "n":
            exit()
        else:
            print("Please select between y or n")
            self.play_again()

    def start(self):

        print(" LET's PLAY BATTLESHIPS ")
        try:
            with open("score.txt", 'r') as f:
                print("Previous Record:")
                data = f.read()
                n_list = data.split('\n')
                n_list.reverse()
            for i in n_list[0:6]:
                if i:
                    val = i.split("-")
                    print(val[0].ljust(30) + "\t\t" + val[1])
        except:
            print("No Previous Record")
        # print("Press ENTER to Start Game !")
        # input()

    def set_up_boards(self, player):

        # clear_screen()
        board = self.boards[player]

        input(f"Pass the computer to player {player}. \nPress enter when ready.")

        print("Enter Name: ")
        self.player_names[player] = input(starter)

        clear_screen()
        ship_names = ["Aircraft carrier", "Cruiser", "Ship", "Frigate", "Submarine"]
        for number, ship in enumerate(self.ships, start=1):
            self.set_up_ships(player, ship, number, ship_names[0])
            ship_names.pop(0)

    def set_up_ships(self, player, ship, number, ship_name):

        board = self.boards[player]

        while True:
            board.display()

            print(
                "\nHere is your board!"
                + f"\nEquipment number {number} is "
                + ship_name
                + f" (length: {ship})"
                + "\nEnter the start point of the equipment (e.g A1)"
            )
            start_point = input(starter).upper()
            print("Enter the orientation of the equipment" "\n Horizontal or Vertical (h/v)")
            orientation = input(starter).upper()

            # Checks
            try:
                start_position = board.echange_pos_var(start_point)
            except BaseException:
                self.show_error("The start position is invalid.")
                continue

            if orientation != "H" and orientation != "V":
                self.show_error("The orientation entered is not either H or V.")
                continue

            current_ship = Ship(start_position, ship, orientation)

            if not board.ship_in_board(current_ship):
                self.show_error("Some of the equipment would fall outside of the board.")
                continue

            if board.collision_check(current_ship):
                self.show_error("The equipment entered collides with another equipment.")
                continue

            board.place_equipment(current_ship)
            board.display()

            print("Would you like to keep the equipment? (C) for confirm.")
            if input(starter).upper() != "C":
                board.delete_equipment(current_ship)
                continue
            else:
                break

    def show_error(self, error):
        print("Error \n {0} Please try again.".format(error))
        input()

    def turn(self, player):

        player_name = self.player_names[player]
        other_player = self.players.replace(player, "")

        board = self.boards[player]
        other_board = self.boards[other_player]

        clear_screen()
        input(f"Pass the computer to {player_name}.Press Enetr when ready.")

        clear_screen()
        print(f"Hello {player_name}.")

        while True:
            self.show_boards(player)

            print("Please enter your guess.")
            guess = input(starter).upper()

            try:
                guess_position = other_board.echange_pos_var(guess)
            except BaseException:
                self.show_error("The position entered is invalid.")
                continue

            if not other_board.on_board(guess_position):
                self.show_error("The guess is outside of the board.")
                continue

            if other_board.guessed(guess_position):
                self.show_error("This position has already been guessed.")
                continue

            result = other_board.guess_position(guess_position)

            if result == hitted_place or result == SUNK:
                if result == hitted_place:
                    print("You HIT Enemy Equipment! ")
                elif result == SUNK:
                    print("You SUNK Enemy Equipment!")

                input()
                if other_board.every_ship_sunked():
                    return True
            elif result == missed_place:
                print("You Hit in Water")
                input()
                break

        else:
            return False

    def show_boards(self, player):
        other_player = self.players.replace(player, "")

        this_board_display = self.boards[player].print_rows(show_ships=True)
        other_board_display = self.boards[other_player].print_rows(show_ships=False)

        text_template = "{}  -- Score: {}"

        player_text = text_template.format(
            self.player_names[player], self.boards[other_player].hits
        )

        other_player_text = text_template.format(
            self.player_names[other_player], self.boards[player].hits
        )

        player_header = center(player_text)
        other_player_header = center(other_player_text)

        print(player_header + (" " * len(board_division)) + other_player_header)

        for this_board, other_board in zip(this_board_display, other_board_display):
            print(this_board + board_division + other_board)


if __name__ == "__main__":
    Game()
