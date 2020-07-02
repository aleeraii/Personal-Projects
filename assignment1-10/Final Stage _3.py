def myMenu():
    print('\n')
    print('______________Menu______________')
    print('\t1) - Category')
    print('\t2) - Item')
    print('\t3) - Serving Size')
    print('\t4) - Calories')
    print('\t5) - Calories from Fat')
    print('\t6) - Total Fat')
    print('\t7) - Cholesterol')
    print('\t8) - Sodium')
    print('\t9) - Carbs')
    print('\t10) - Protein')
    print('\t11) - Sugar')
    print('\t12) - Done')


def processInput(results,data):
    headings =['Category' ,'Item' ,'Serving Size' ,'Calories' ,'Calories from Fat' ,'Total Fat' ,'Cholesterol', \
              'Sodium' ,'Carbs' ,'Protein' ,'Sugars']

    print('The user entered choice: {0} - {1}'.format(results ,headings[results-1]))
    print()
    if 1 <= results <= 3:
        sortData = sorted(data, key = lambda r :(str(r[results -1])), reverse = True)
        top5 = 0
        print("Top 5 Items:\n")
        for count in range(5):
            top5 +=1
            print(" {}| {} {}".format(top5, sortData[count][1], sortData[count][results -1]))
    elif 4 <= results <= 5 or 7 <= results <= 11:
        sortData = sorted(data, key=lambda r: (int(r[results - 1])), reverse=True)
        top5 = 0
        print("Top 5 Items:\n")
        for count in range(5):
            top5 += 1
            print(" {}| {} {}".format(top5, sortData[count][1], sortData[count][results - 1]))
    elif results == 6:
        sortData = sorted(data, key=lambda r: (float(r[results - 1])), reverse=True)
        top5 = 0
        print("Top 5 Items:\n")
        for count in range(5):
            top5 += 1
            print(" {}| {} {}".format(top5, sortData[count][1], sortData[count][results - 1]))
    else:
        pass


def printMenu():
    while True:
        try:
            myMenu()
            choice = int(input('Enter a number between 1 and 12: '))
            if choice > 12:
                print('Enter a number between 1 and 12: ')
            else:
                return choice
        except ValueError:
            print('Invalid number enter.')


def main():
    while True:
            data = []
            infile = open("Mac_menu.csv", "r")
            line = infile.readline()
            for line in infile:
                line = line.rstrip("\n")
                result = tuple(line.split(","))
                data.append(result)
            infile.close()
            choice = printMenu()
            if choice == 12:
                exit()
            else:
                processInput(choice,data)


main()
