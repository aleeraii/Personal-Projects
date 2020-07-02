import random, time


class Grid:
    def __init__(self, width, height):
        self.grid = []
        self.pieces = [[0], [1], [2], ["miss"], ["hit"]]
        for y in range(height):
            row = []
            for x in range(width):
                row.append("")
            self.grid.append(row)

    def addPiece(self,piece,side):
        for pieceSet in self.pieces:
            if pieceSet[0] == side:
                pieceSet.append(piece)

        for coord in piece:
            self.grid[coord[1]][coord[0]] = side

    def isDefeated(self,side):
        for row in self.grid:
            for piece in row:
                if piece == side:
                    return False
        return True

    def show(self):
        # print("-" * 45)
        line = ""
        for i in range(10):
            line += "  " + str(i) + " "
        print(line + "     ")
        # print("-" * 45)
        cord = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for y in range(len(self.grid)):
            line = ""
            for x in self.grid[y]:
                if x == "":
                    line += "  - "
                elif x == 0:
                    line += "  - "
                elif x == 1:
                    line += "  - "
                elif x == 2:
                    line += "  - "
                elif x == "miss":
                    line += "  X "
                elif x == "hit":
                    line += "  O "

            # Adding side coordinates

            line += "  " + cord[0] + "  \n"
            cord.pop(0)
            # for x in self.grid[y]:
            #     line += "----"
            # line += "-----"
            print(line)

    def isEmpty(self, x, y):
        if self.grid[y][x] == "":
            return True
        else:
            return False

    def getCoordValue(self,x,y):
        return self.grid[y][x]


class Battleships:

    def __init__(self):
        self.PVE()

    def addShip(self, grid, side, length):

        orientation = 0
        while orientation < 1 or orientation > 2:
            try:
                orientation = int(input("Would you like the ship to be horizontal [1] or vertical [2]: "))
            except:
                orientation = 0

        if orientation == 1:
            rootCoord = self.inputCoord(10-length, 9)
        elif orientation == 2:
            rootCoord = self.inputCoord(9, 10-length)

        ship = []

        while True:
            currentShip = []
            # Add coords depending on length

            for i in range(length):
                if orientation == 1:
                    currentShip.append([rootCoord[0]+i,rootCoord[1]])
                elif orientation == 2:
                    currentShip.append([rootCoord[0], rootCoord[1]+i])

            # Test that the coords are not filled already
            validShip = True
            for coord in currentShip:
                if grid.isEmpty(coord[0],coord[1]) == False:
                    # If any coords are filled then the ship is invalid

                    validShip = False
                    print("There are already ships existing there!")
                    return self.addShip(grid, side, length)


            # If ship is valid then stop trying and return ship coords

            if validShip:
               ship = currentShip
               return ship

    # Function returns list of ship lengths that has been sunk

    def getSunkShips(self,grid,side):

        # List of sunk ships

        sunkShips = []

        # Go through the pieces array in grid object
        for ship in range(1,len(grid.pieces[side])):
            sunkStatus = []

            # For each ship coordinate in a ship

            for shipCoord in grid.pieces[side][ship]:

                # If the coordinate can be found in the hit list then that part has been sunk

                sunk = False
                for hitCoord in range(1,len(grid.pieces[4])):
                    if shipCoord == grid.pieces[4][hitCoord][0]:
                        sunk = True
                        break
                sunkStatus.append(sunk)

            # Go through the sunk parts and if all of it is sunk then the ship is sunk

            sunkShip = True
            for status in sunkStatus:
                if status == False:
                    sunkShip = False
                    break

            if sunkShip == True:
                sunkShips.append(ship+1)
        return sunkShips

    # Method for when the user wants to play against the computer

    def PVE(self):

        # Create grids

        grids = [Grid(10, 10), Grid(10, 10)]

        print("____________________________ Welcome To Player Vs Computer ____________________________")

        # Add ships for player 1

        print("-- Add Your Equipments --")

        ship_names = ["Aircraft carrier", "Cruiser", "Ship", "Frigate", "Submarine"]
        shipLength = 5
        for ship in ship_names:
            print("Add {0} of length {1}".format(ship, shipLength))
            ship = self.addShip(grids[0], 1, shipLength)
            grids[0].addPiece(ship, 1)
            shipLength -= 1
            input("Press Enter to Add Next Equipment")
        self.clear_screen()
        print("Okay, the grids are set!")
        # self.clear_screen()

        # Add ships for computer

        grids[1].grid = self.makeShips(grids[1],0,[1,1,1,1,1])


        turn = 1

        # Lists of coords the computer should shoot next

        compWaitList = [[]]

        # Coords the computer has tried
        compShotList = []
        compSunkShips = []
        compPreviousHits = []

        # While there are ships on both side

        while grids[0].isDefeated(1) == False and grids[1].isDefeated(0) == False:

            # If it is player 1's turn

            if turn == 1:

                print("Player 1's turn to shoot.")
                grids[1].show()
                validMove = False

                while validMove == False:

                    # Get shot input and try to shoot
                    # If shot is not invalid then update the grid

                    shot = self.inputCoord(9,9)
                    potentialGrid = self.shoot(grids[1],0,shot)

                    if potentialGrid != "invalid":
                        grids[1].grid = potentialGrid
                        validMove = True
                    else:
                        continue

                input("Press enter to continue.")
                self.clear_screen()
                print("Current grid for Player 1.")
                grids[1].show()

                # Check game is won or not


                if grids[1].isDefeated(0) == True:
                    self.clear_screen()
                    print("Player 1 wins!")
                    input("Press enter to continue...")
                    self.clear_screen()
                    break

                # If game is not won, tell the players of any full ships they have sunk.

                self.sunkShips = self.getSunkShips(grids[1], 0)
                if len(self.sunkShips) >= 1:
                    pass
                    # print("Player 1 has sunk...")
                    for ship in self.sunkShips:
                        pass
                        # print("Ship of length {}.".format(ship))
                else:
                    print("No ships have yet been sunk.")

                input("Press enter for Computer's turn.")
                self.clear_screen()
                turn = 2

            # Computer's turn

            if turn == 2:

                print("Computer's turn to shoot.")

                validShot = False

                # Get a possible x and y coordinate to shoot

                while validShot == False:

                    x = -1
                    y = -1

                    if compWaitList == [[]]:
                        while x < 0 or x > 9:
                            x = random.randint(0,9)

                        while y < 0 or y > 9:
                            y = random.randint(0,9)

                    # Else take the first coord from the waiting list

                    else:
                        if compWaitList[0] != []:
                            x = compWaitList[0][0][0]
                            y = compWaitList[0][0][1]
                            compWaitList[0].pop(0)
                        else:
                            x = compWaitList[1][0][0]
                            y = compWaitList[1][0][1]
                            compWaitList[1].pop(0)

                    alreadyShot = False

                    # If proposed x and y coordinate is in shot list then repeat loop
                    for coord in compShotList:
                        if coord == [x,y]:
                            alreadyShot = True
                            break

                    if alreadyShot == False:
                        validShot = True

                print("Computer is deciding...")
                time.sleep(1)

                # Shoot with coords and also add them to used coords

                compShotList.append([x,y])
                potentialGrid = self.shoot(grids[0],1,[x,y],True)
                print("Computer shot at [{},{}].".format(x,y))

                # If it was a hit then try adding smart coords to wait list

                if potentialGrid[1] == "hit":
                    print("The computer hit!")
                    grids[0].show()

                    # If there has been previous hit of importance and there are still possible hit locations
                    if compPreviousHits != [] and compWaitList != []:

                        # If the number of sunk ship increases, get the sunk length then remove the last n-1 possible perpendicular coords

                        if compSunkShips != self.getSunkShips(grids[0],1):
                            sunkShipLength = self.getSunkShips(grids[0],1)
                            print(compSunkShips)
                            print(sunkShipLength)
                            for length in compSunkShips:
                                if sunkShipLength[0] == length:
                                    sunkShipLength.pop(0)

                            compSunkShips = self.getSunkShips(grids[0],1)
                            compWaitList[0] = []

                            # Move the previous hit to last, to be removed

                            compPreviousHits.append(compPreviousHits[0])
                            compPreviousHits.pop(0)
                            compPreviousHits.append([x,y])

                            del compWaitList[len(compWaitList)-sunkShipLength[0]:]

                            if compWaitList == []:
                                compWaitList.append([])
                            del compPreviousHits[len(compPreviousHits)-sunkShipLength[0]:]

                        # Else find relation of the two coords
                        else:

                            # Set limits to relating to whether they're on the edge and tets relation to last hit

                            if compPreviousHits[0][0] == x:

                                # Add next parallel coord (in relation to the hit and previosuly hit coord) to high priority, and perpendicular coords to lowest priority
                                # This is so there is a higher probability of another hit

                                if compPreviousHits[0][1] < y:
                                    compWaitList += [[[[x+1,y],[x-1,y]]]]
                                    if y != 9:
                                        compWaitList[0] = [[[x,y+1]]] + compWaitList[0]
                                else:
                                    compWaitList += [[[[x+1,y],[x-1,y]]]]
                                    if y != 0:
                                        compWaitList[0] = [[x,y-1]] + compWaitList[0]

                            elif compPreviousHits[0][1] == y:
                                if compPreviousHits[0][0] < x:
                                    compWaitList += [[[x,y-1],[x,y+1]]]
                                    if x != 9:
                                        compWaitList[0] = [[x+1,y]] + compWaitList[0]
                                else:
                                    compWaitList += [[[x,y-1],[x,y+1]]]
                                    if x != 0:
                                        compWaitList[0] = [[x-1,y]] + compWaitList[0]

                            compPreviousHits.append(compPreviousHits[0])
                            compPreviousHits.pop(0)
                            compPreviousHits = [[x,y]] + compPreviousHits
                    else:

                        # Add adjacent coords to the waiting list, depending on position on the grid
                        if x == 0:
                            if y == 0:
                                compWaitList[0] = [[x+1,y]]
                                compWaitList.append([[x,y+1]])
                            elif y == 9:
                                compWaitList[0] = [[x+1,y]]
                                compWaitList.append([[x,y-1]])
                            else:
                                compWaitList[0] = [[x+1,y]]
                                compWaitList.append([[x,y-1],[x,y+1]])
                        elif x == 9:
                            if y == 0:
                                compWaitList[0] = [[x-1,y]]
                                compWaitList.append([[x,y+1]])
                            elif y == 9:
                                compWaitList[0] = [[x-1,y]]
                                compWaitList.append([[x,y-1]])
                            else:
                                compWaitList[0] = [[x-1,y]]
                                compWaitList.append([[x,y-1],[x,y+1]])
                        elif y == 0:
                            compWaitList[0] = [[x-1,y]]
                            compWaitList.append([[x+1,y],[x,y+1]])
                        elif y == 9:
                            compWaitList[0] = [[x-1,y]]
                            compWaitList.append([[x+1,y],[x,y-1]])
                        else:
                            compWaitList[0] = [[x-1,y]]
                            compWaitList.append([[x+1,y],[x,y-1],[x,y+1]])

                        compPreviousHits.append([x,y])

                    grids[0].grid = potentialGrid[0]
                    validMove = True
                else:
                    print("The computer missed!")
                    grids[0].show()

                # Check game is won or not

                if grids[0].isDefeated(1) == True:
                    self.clear_screen()
                    grids[0].show()
                    print("Player 2 wins!")
                    input("Press enter to continue...")
                    self.clear_screen()
                    break

                self.sunkShips = self.getSunkShips(grids[0],1)
                if len(self.sunkShips) >= 1:
                    pass
                    for ship in self.sunkShips:
                        pass
                        # print("Ship of length {}.".format(ship))
                else:
                    pass

                input("Press enter for Player 1's turn.")
                self.clear_screen()
                turn = 1


        return

    # Function takes in a grid, the opposing side, and the coordinates for the shot

    def shoot(self, grid, oSide, shot, isComputer=False):

        # Get value in the coord to be shot
        coordValue = grid.getCoordValue(shot[0],shot[1])

        # If the opponent is the computer

        if oSide == 0:

            # If value is miss or hit, it is an invalid move

            if coordValue == "miss":
                print("You've already shot there! Was a miss!")
                return "invalid"
            elif coordValue == "hit":
                print("You've already shot there! Was a hit!")
                return "invalid"

            # If blank, miss

            elif coordValue == "":
                print("Miss!")
                grid.addPiece([shot],"miss")
                return grid.grid

            # If computer piece, hit

            elif coordValue == 0:
                print("Hit!")
                grid.addPiece([shot],"hit")
                return grid.grid

        elif oSide == 1:
            if isComputer == True:
                if coordValue == "":
                    grid.addPiece([shot],"miss")
                    return [grid.grid,"miss"]
                elif coordValue == 1:
                    grid.addPiece([shot],"hit")
                    return [grid.grid,"hit"]
            else:
                if coordValue == "miss":
                    print("You've already shot there! Was a miss!")
                    return "invalid"
                elif coordValue == "hit":
                    print("You've already shot there! Was a hit!")
                    return "invalid"

                # If shooting at side 2 (own), then it is invalid

                elif coordValue == 2:
                    print("You cannot shoot your own ships!")
                    return "invalid"
                elif coordValue == "":
                    print("Miss!")
                    grid.addPiece([shot],"miss")
                    return grid.grid

                # If opponet is 1 and you shoot 1 then it is hit

                elif coordValue == 1:
                    print("Hit!")
                    grid.addPiece([shot],"hit")
                    return grid.grid

        elif oSide == 2:
            if coordValue == "miss":
                print("You've already shot there! Was a miss!")
                return "invalid"
            elif coordValue == "hit":
                print("You've already shot there! Was a hit!")
                return "invalid"

            # If shooting at side 1 (own), then it is invalid

            elif coordValue == 1:
                print("You cannot shoot your own ships!")
                return "invalid"
            elif coordValue == "":
                print("Miss!")
                grid.addPiece([shot],"miss")
                return grid.grid

            # If opponet is 2 and you shoot 2 then it is hit

            elif coordValue == 2:
                print("Hit!")
                grid.addPiece([shot],"hit")
                return grid.grid

    def makeShips(self, grid, side, shipLengths):
        for length in range(1, len(shipLengths)+1):
            ship = self.makeShip(grid,length)
            grid.addPiece(ship,side)
        return grid.grid

    def makeShip(self,grid,length):
        ship = []

        orientation = random.randint(1,2)

        while True:
            currentShip = []

            # Get root position depending on orientation

            if orientation == 1:
                x = random.randint(0,10-length)
                y = random.randint(0,9)
            elif orientation == 2:
                x = random.randint(0,9)
                y = random.randint(0,10-length)

            # Add coords depending on length

            for i in range(length):
                if orientation == 1:
                    currentShip.append([x+i,y])
                elif orientation == 2:
                    currentShip.append([x,y+i])

            # Test that the coords are not filled already

            validShip = True
            for coord in currentShip:
                if grid.isEmpty(coord[0],coord[1]) == False:

                    # If any coords are filled then the ship is invalid

                    validShip = False

            # If ship is valid then stop trying and return ship coords

            if validShip:
               keepTrying = False
               ship = currentShip
               return ship

    # Function takes in coordinate inputs

    def inputCoord(self, maxX, maxY):
        x = -1
        y = -1

        # While the coordinates are not within grid params

        while x < 0 or x > maxX:
            try:
                x = int(input("Enter X coordinate: "))
            except:
                x = -1

        while y < 0 or y > maxY:
            try:
                y = int(input("Enter Y coordinate: "))
            except:
                y = -1

        return [x, y]

    def clear_screen(self):
        print("\n" * 100)


game = Battleships()