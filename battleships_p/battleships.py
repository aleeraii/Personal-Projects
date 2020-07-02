from itertools import cycle
from board import Board
from const import LINE_LENGTH, START_SHIPS, SIZE, PROMPT
from const import HIT, MISS, SUNK, BOARD_SEPERATOR
from const import Ship
from pve import *


def clear_screen():
    print("\n" * 100)


def center(text, width=LINE_LENGTH):

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
        print(winning_player + " é o VENCEDOR !!!")
        other_player = self.players.replace(player, "")
        with open("record.txt", 'a') as f:
            f.write(winning_player+"-"+str(self.boards[other_player].hits)+"\n")


    def welcome(self):
        print("________________________ BATALHAS ________________________ \n")
        try:
            with open("record.txt", 'r') as f:
                data = f.read()
                n_list = data.split('\n')
                n_list.reverse()
                print("Pontuações recentes:")
            for i in n_list[0:6]:
                if i:
                    val = i.split("-")
                    print(val[0].ljust(30) + "\t\t" + val[1])
        except:
            print("Nenhum registro anterior")
        print("Pressione ENTER para iniciar o jogo!")
        input()

    def set_up(self, player):

        clear_screen()
        board = self.boards[player]

        input(f"Passe o computador para o player {player}. Pressione ENTER quando estiver pronto.")

        print("Qual é o seu nome ?")
        self.player_names[player] = input(PROMPT)

        clear_screen()
        ship_names = ["Aircraft carrier", "Cruiser", "Ship", "Frigate", "Submarine"]
        for number, ship in enumerate(self.ships, start=1):
            self.set_ship(player, ship, number, ship_names[0])
            ship_names.pop(0)

    def set_ship(self, player, ship, number, ship_name):
        board = self.boards[player]

        while True:
            board.display()

            print(
                "\nAqui está o seu quadro!"
                + f"\nNúmero do equipamento {number} é "
                + ship_name
                + f" (comprimento: {ship})"
                + "\nDigite o ponto inicial do equipamento (i.e., A1)"
            )
            start_point = input(PROMPT).upper()
            print("Digite a orientação do equipamento" "\n(H) horizontal ou (V) vertical")
            orientation = input(PROMPT).upper()

            # Checks
            try:
                start_position = board.convert_position(start_point)
            except BaseException:
                self.print_error("A posição inicial é inválida.")
                continue

            if orientation != "H" and orientation != "V":
                self.print_error("A orientação inserida não é H ou V.")
                continue

            current_ship = Ship(start_position, ship, orientation)

            if not board.is_ship_on_board(current_ship):
                self.print_error("Alguns dos equipamentos ficariam fora do quadro.")
                continue

            if board.check_ship_collisions(current_ship):
                self.print_error("O equipamento inserido colide com outro equipamento.")
                continue

            board.place_ship(current_ship)
            board.display()

            print("Deseja manter o equipamento? (C) para confirmar.")
            if input(PROMPT).upper() != "C":
                board.delete_ship(current_ship)
                continue
            else:
                break

    def print_error(self, error):
        print("Erro \n {0} Por favor, tente novamente.".format(error))
        input()

    def round(self, player):

        player_name = self.player_names[player]
        other_player = self.players.replace(player, "")

        board = self.boards[player]
        other_board = self.boards[other_player]

        clear_screen()
        input(f"Passe o computador para {player_name}. Pressione ENTER quando estiver pronto.")

        clear_screen()
        print(f"Olá {player_name}.")

        while True:
            self.display_both_boards(player)

            print("Digite seu palpite.")
            guess = input(PROMPT).upper()

            try:
                guess_position = other_board.convert_position(guess)
            except BaseException:
                self.print_error("A posição inserida é inválida.")
                continue

            if not other_board.is_on_board(guess_position):
                self.print_error("O palpite está fora do quadro.")
                continue

            if other_board.is_guessed(guess_position):
                self.print_error("Esta posição já foi adivinhada.")
                continue

            result = other_board.guess_position(guess_position)

            if result == HIT or result == SUNK:
                if result == HIT:
                    print("Você BATE Equipamento Inimigo! ")
                elif result == SUNK:
                    print("Você afunda equipamentos inimigos! ÓTIMO")

                input()
                if other_board.all_ships_sunk():
                    return True
            elif result == MISS:
                print("Você bate na água")
                input()
                break

        else:
            return False

    def display_both_boards(self, player):

        other_player = self.players.replace(player, "")

        this_board_display = self.boards[player].print_rows(show_ships=True)
        other_board_display = self.boards[other_player].print_rows(show_ships=False)

        text_template = "{}  | Ponto: {}"

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


def main():
    while True:
        try:
            print("1- Player Vs Player\n2- Player Vs Computer ")
            sel = int(input("Please Select An Option: "))
            if sel == 1:
                Game()
                break
            elif sel == 2:
                Battleships()
                break
        except:
            print("Please Chose Between 1 abd 2")


if __name__ == "__main__":
    main()

    def play_again():
        val = input("Você quer jogar de novo? (y/n)")
        if val.lower() == "y":
            main()
        elif val.lower() == "n":
            exit()
        else:
            print("Por favor, selecione entre y ou n")
            play_again()
    play_again()