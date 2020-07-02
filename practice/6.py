import time
from threading import Thread
import queue
q = queue.LifoQueue()


# this function receives the two lists from the merge_sort function and check between the elements of the list that
# which one must comes first than other. The main sorting is done in this function.
def merge(larr, rarr, val):
    result = []
    if val == 1:
        while len(larr) > 0 < len(rarr):
            if larr[0].name[0] <= rarr[0].name[0]:
                result.append(larr[0])
                larr.pop(0)
            else:
                result.append(rarr[0])
                rarr.pop(0)
        for i in larr:
            result.append(i)
        for i in rarr:
            result.append(i)
        return result
    elif val == 2:
        while len(larr) > 0 < len(rarr):
            if larr[0].city[0] <= rarr[0].city[0]:
                result.append(larr[0])
                larr.pop(0)
            else:
                result.append(rarr[0])
                rarr.pop(0)
        for i in larr:
            result.append(i)
        for i in rarr:
            result.append(i)
        return result
    elif val == 3:
        while len(larr) > 0 < len(rarr):
            if larr[0].food[0] <= rarr[0].food[0]:
                result.append(larr[0])
                larr.pop(0)
            else:
                result.append(rarr[0])
                rarr.pop(0)
        for i in larr:
            result.append(i)
        for i in rarr:
            result.append(i)
        return result
    elif val == 4:
        while len(larr) > 0 < len(rarr):
            if larr[0].team[0] <= rarr[0].team[0]:
                result.append(larr[0])
                larr.pop(0)
            else:
                result.append(rarr[0])
                rarr.pop(0)
        for i in larr:
            result.append(i)
        for i in rarr:
            result.append(i)
        return result


# this is the starting point for the algorithm. It takes in an array or list and divide it into two part and recursively
# calls it self to keep dividing the list until all the elements are split. It also calls the merge function for
# each split list and get sorted list from that. This function is not using any threads
def merge_sort2(array, val):
    if len(array) <= 1:
        return array
    else:
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]
        left = merge_sort2(left, val)
        right = merge_sort2(right, val)
        return merge(left, right, val)


# this is the same merge sort function but with arrays and it also takes q variable as parameter
def merge_sort(array, q, val):
    if len(array) <= 1:
        return array
    else:
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]
        th1 = Thread(target=lambda que, arg1: que.put(merge_sort2(arg1, val)), args=(q, left))
        th2 = Thread(target=lambda que, arg1: que.put(merge_sort2(arg1, val)), args=(q, right))
        th1.setDaemon(True)
        th2.setDaemon(True)
        th1.start()
        th2.start()
        th1.join()
        th2.join()
        return merge(q.get(), q.get(), val)


def manage():
    class Info:
        def __init__(self, name, city, food, team):
            self.name = name
            self.city = city
            self.food = food
            self.team = team

        def __repr__(self):
            return '({}, {}, {}, {})'.format(self.name, self.city, self.food, self.team)

    Info1 = Info("John", "hfd", "burger", "LQ")
    Info2 = Info("Alex", "fsd", "pizza", "KK")
    Info3 = Info("Wick", "isb", "tacos", "PZ")
    Info4 = Info("Kathie", "lhr", "icecream", "IU")
    info = [Info1, Info2, Info3, Info4]
    while True:
        try:
            val = int(input("How do you want to sort the array?\n"
                            "1- By Name\n"
                            "2- By City\n"
                            "3- By Food\n"
                            "4- By Team\n"
                            "Please Enter Your Selection: "))
            if val == 1:
                infos = [Info1.name, Info2.name, Info3.name, Info4.name]
                break
            elif val == 2:
                infos = [Info1.city, Info2.city, Info3.city, Info4.city]
                break
            elif val == 3:
                infos = [Info1.food, Info2.food, Info3.food, Info4.food]
                break
            elif val == 4:
                infos = [Info1.team, Info2.team, Info3.team, Info4.team]
                break
            else:
                print("Wrong Choice")
        except:
            print("Only Integers are allowed")
    return infos, info, val


# the main function controls all the execution sequence of the program
def main():
    infos, info, val = manage()
    print("Unsorted Array:\n" + str(info))
    t1 = time.time()
    x = merge_sort(info, q, val)
    total = time.time()-t1
    t2 = time.time()
    merge_sort2(info, val)
    total2 = time.time() - t2
    print("Sorted Array:\n" + str(x))
    print("Time Taken By Merge Sort With Threads: " + str(total))
    print("Time Taken By Merge Sort Without Threads: " + str(total2))


# this is where execution of program begins
if __name__ == '__main__':
    main()