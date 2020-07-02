import random


def roll_dice():
    a = random.randrange(1, 7)
    b = random.randrange(1, 7)
    return a+b


def play_again():
    val = input("Do you want to play again ? (y/n)")
    if val.lower() == "y":
        main()
    elif val.lower() == "n":
        exit()
    else:
        print("Please select between y or n")
        play_again()


def play_two(count):
    score = {}
    for key, value in count.items():
        turn = turns(value, key)
        score[key] = turn
    winner_name = ''
    winner_val = 0
    for key, value in score.items():
        if value is None:
            pass
        else:
            if winner_val == 0:
                winner_val = value
                winner_name = key
            else:
                if value < winner_val:
                    winner_val = value
                    winner_name = key
                else:
                    pass

    for k, v in score.items():
        if v != winner_val and v is not None:
            print("Player {0} lost by score {1}".format(k,v))
        elif v is None:
            print("Player {0} rolled 7 or 11 after first roll and lost".format(k))
        else:
            print("The winner was Player {0} with minimum score of {1}".format(winner_name, winner_val))
    play_again()


def re_roll(count):
    val = input("Do you want to Re Roll ? (y/n)")
    if val.lower() == "y":
        play_two(count)
    elif val.lower() == "n":
        exit()
    else:
        print("Please select between y or n")
        re_roll(count)


def turns(point, i):
    turn = 1
    while True:
        dice = roll_dice()
        # time.sleep(1)
        print("Rolling Dice For Player {0} ... {1}".format(i, dice))
        if dice == 7 or dice == 11:
            return None
        if dice == point:
            turn += 1
            break
        else:
            turn += 1

    return turn


def play(p_num):
    count = {}
    for i in range(1, p_num + 1):
        dice = roll_dice()
        print("Rolling Dice For Player {0} ... {1}".format(i, dice))
        count[i] = dice
    winner_name = ''
    winner_val = 0
    for key, value in count.items():
        if winner_val == 0:
            if value == 7 or value == 11:
                winner_name = key
                winner_val = value
    if winner_val != 0:
        print("The winner was Player {0} with roll of {1}".format(winner_name, winner_val))
        play_again()
    else:
        print("No One Rolled 7 or 11")
        re_roll(count)


def main():
    print("\n\n_____________ Welcome to Dice Game _____________ ")
    while True:
        try:
            p_num = int(input("How many players are there ? (1-4) "))
            if p_num == 1 or p_num == 2 or p_num == 3 or p_num == 4:
                break
            else:
                print("Kindly Select 1 to 4 number of players")
        except ValueError:
            print("ONLY INTEGERS ARE ALLOWED")
    play(p_num)


main()
