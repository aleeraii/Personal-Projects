from itertools import cycle
from board import Board
from const import LINE_LENGTH, START_SHIPS, SIZE, PROMPT
from const import HIT, MISS, SUNK, BOARD_SEPERATOR
from const import Ship


def clear_screen():
    """Clear the screen."""

    print("\n" * 100)


def center(text, width=LINE_LENGTH):
    """Centre colorful strings."""

    length = len(text)
    start = (width - length) // 2
    end = width - length - start
    output = (" " * start) + text + (" " * end)
    return output


class Game:
    def __init__(self):
        """Set up key variables and play the game."""

        # Set up the variables
        self.players = "AB"
        self.player_names = {}
        self.boards = {player: Board(SIZE) for player in self.players}
        self.ships = START_SHIPS
        self.welcome()

        for player in self.players:
            self.set_up(player)
        # Play the game
        for player in cycle(self.players):
            if self.round(player):
                break

        winning_player = self.player_names[player]
        print(winning_player + " is the WINNER!!!")
        other_player = self.players.replace(player, "")
        with open("record.txt", 'a') as f:
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

    def welcome(self):
        """Print the initial input screen and wait for initial input."""

        print("________________________ BATTLESHIPS ________________________ \nRecent Scores:")
        with open("record.txt", 'r') as f:
            data = f.read()
            n_list = data.split('\n')
            n_list.reverse()
        for i in n_list[0:6]:
            if i:
                val = i.split("-")
                print(val[0].ljust(30) + "\t\t" + val[1])
        print("Press ENTER to Start Game !")
        input()

    def set_up(self, player):
        """Allow the players to set up their screens."""

        clear_screen()
        board = self.boards[player]

        input(f"Pass the computer to player {player}. Hit ENTER when ready.")

        print("What would you like to be called?")
        self.player_names[player] = input(PROMPT)

        clear_screen()
        ship_names = ["Aircraft carrier", "Cruiser", "Ship", "Frigate", "Submarine"]
        for number, ship in enumerate(self.ships, start=1):
            self.set_ship(player, ship, number, ship_names[0])
            ship_names.pop(0)

    def set_ship(self, player, ship, number, ship_name):
        """Set up one ship, including validating input."""

        board = self.boards[player]

        while True:
            board.display()

            print(
                "\nHere is your board!"
                + f"\nEquipment number {number} is "
                + ship_name
                + f" (length: {ship})"
                + "\nEnter the start point of the equipment (i.e., A1)"
            )
            start_point = input(PROMPT).upper()
            print("Enter the orientation of the equipment" "\n(H)orizontal or (V)ertical")
            orientation = input(PROMPT).upper()

            # Checks
            try:
                start_position = board.convert_position(start_point)
            except BaseException:
                self.print_error("The start position is invalid.")
                continue

            if orientation != "H" and orientation != "V":
                self.print_error("The orientation entered is not either H or V.")
                continue

            current_ship = Ship(start_position, ship, orientation)

            if not board.is_ship_on_board(current_ship):
                self.print_error("Some of the equipment would fall outside of the board.")
                continue

            if board.check_ship_collisions(current_ship):
                self.print_error("The equipment entered collides with another equipment.")
                continue

            board.place_ship(current_ship)
            board.display()

            print("Would you like to keep the equipment? (C) for confirm.")
            if input(PROMPT).upper() != "C":
                board.delete_ship(current_ship)
                continue
            else:
                break

    def print_error(self, error):
        """Print the error message if invalid input."""
        print("Error \n {0} Please try again.".format(error))
        input()

    def round(self, player):
        """Go through one round of battleships."""

        player_name = self.player_names[player]
        other_player = self.players.replace(player, "")

        board = self.boards[player]
        other_board = self.boards[other_player]

        clear_screen()
        input(f"Pass the computer to {player_name}. Hit ENTER when ready.")

        clear_screen()
        print(f"Hello {player_name}.")

        while True:
            self.display_both_boards(player)

            print("Please enter your guess.")
            guess = input(PROMPT).upper()

            try:
                guess_position = other_board.convert_position(guess)
            except BaseException:
                self.print_error("The position entered is invalid.")
                continue

            if not other_board.is_on_board(guess_position):
                self.print_error("The guess is outside of the board.")
                continue

            if other_board.is_guessed(guess_position):
                self.print_error("This position has already been guessed.")
                continue

            result = other_board.guess_position(guess_position)

            if result == HIT or result == SUNK:
                if result == HIT:
                    print("You HIT Enemy Equipment! ")
                elif result == SUNK:
                    print("You SUNK Enemy Equipment! GREAT")

                input()
                if other_board.all_ships_sunk():
                    return True
            elif result == MISS:
                print("You Hit in Water")
                input()
                break

        else:
            return False

    def display_both_boards(self, player):
        """Display the current board on the left and the other board on the right."""

        other_player = self.players.replace(player, "")

        this_board_display = self.boards[player].print_rows(show_ships=True)
        other_board_display = self.boards[other_player].print_rows(show_ships=False)

        text_template = "{}  | Score: {}"

        player_text = text_template.format(
            self.player_names[player], self.boards[other_player].hits
        )

        other_player_text = text_template.format(
            self.player_names[other_player], self.boards[player].hits
        )

        player_header = center(player_text)
        other_player_header = center(other_player_text)

        print(player_header + (" " * len(BOARD_SEPERATOR)) + other_player_header)

        for this_board, other_board in zip(this_board_display, other_board_display):
            print(this_board + BOARD_SEPERATOR + other_board)


if __name__ == "__main__":
    Game()
