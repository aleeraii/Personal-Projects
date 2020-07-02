import time                                         # this library is used to record the time difference
import random                                       # this library is used to generate random values for input list
from threading import *                             # the main threading module to create threads
import queue                                        # this library is used to put thread results in queue
q = queue.LifoQueue()                               # initiating the queue in a variable


# this function receives the two lists from the merge_sort function and check between the elements of the list that
# which one must comes first than other. The main sorting is done in this function.
def merge(larr, rarr):
    result = []     # this list is used to store the final sorted result
    while len(larr) > 0 < len(rarr):    # checking the length of inputs that must be greater than zero
        if larr[0] <= rarr[0]:          # now finding the smaller number and putting in the list first
            result.append(larr[0])
            larr.pop(0)
        else:
            result.append(rarr[0])
            rarr.pop(0)
    for i in larr:                     # after comparison if any of the elements are left in the input lists, those are
        result.append(i)               # pushed in this list
    for i in rarr:
        result.append(i)
    return result


# this is the starting point for the algorithm. It takes in an array or list and divide it into two part and recursively
# calls it self to keep dividing the list until all the elements are split. It also calls the merge function for
# each split list and get sorted list from that. This function is not using any threads
def merge_sort2(array):
    if len(array) <= 1:     # this condition will return the same list back if it is true
        return array
    else:
        mid = len(array) // 2       # dividing the list into two
        left = array[:mid]          # making a new list from first half of original list
        right = array[mid:]         # making a new list from second half of original list
        left = merge_sort2(left)    # giving a recursive call on first half list
        right = merge_sort2(right)  # giving a recursive call on second half list
        return merge(left, right)   # both the halves are sent to merge function to sort them accordingly


# this is the same merge sort function but with arrays and it also takes q variable as parameter
def merge_sort(array, q):
    if len(array) <= 1:
        return array
    else:
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]
        th1 = Thread(target=lambda que, arg1: que.put(merge_sort2(arg1)), args=(q, left))   # creating first thread and calling the maerge sort function without threads
        th2 = Thread(target=lambda que, arg1: que.put(merge_sort2(arg1)), args=(q, right))
        th1.start()     # here we are starting the created threads
        th2.start()
        th1.join()      # once the thread are completed executing, join is used to turn them off
        th2.join()
        return merge(q.get(), q.get())  # sending resulted broken pieces of original list to merge.


# the main function controls all the execution sequence of the program
def main():
    num = [random.randrange(1000) for x in range(2000)]
    print("Unsorted Array:\n" + str(num))
    t1 = time.time()
    merge_sort(num, q)
    total = time.time()-t1
    t2 = time.time()
    x = merge_sort2(num)
    total2 = time.time() - t2
    print("Sorted Array:\n" + str(x))
    print("Time Taken By Merge Sort With Threads: " + str(total))
    print("Time Taken By Merge Sort Without Threads: " + str(total2))


# this is where execution of program begins
if __name__ == '__main__':
    main()
