import threading
import socket
import math
import time

NUM_OF_PORTS = 65535
ports_scanned = [False] * NUM_OF_PORTS
HOST = 'https://www.hackthissite.org/'
##You can scan any other server you are authorized to scan.
##Please note that it might be illigal to scan a server without permission.
##You can safely scan hackthissite.org

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def scan_port(port):
    """This function tries to connect to the given port.
    It returns True if can, False otherwise."""
    if port <= 0 or port > NUM_OF_PORTS:
        return
    try:
        s.connect((HOST, port))
        return True
    except:
        return False


def scan_range(start, end):
    """Scans a range of ports"""
    #your code goes here
    #use the scan_port function
    #mark the port you scan as True in ports_scanned list
    pass


def threaded_scan(num_of_threads):
    """This functions scans all 65535 ports using the given number of threads.
    Each thread scans almost the same numer of ports."""
    #your code goes here
    #create num_of_threads threads
    #make each thread call scan_range function with the correct range it is responsbible for
    #make sure you divide the whole range correctly, for example if you have 2 threads, the first thread should scan the first half of the range of ports, and the second thread should scan the second part. and so on.
    pass


def main():
    """Times how long it takes to scan all ports using different numbers of threads.
    Checks that all ports are scanned in each case."""
    #your code goes here
    #For a given number of threads do the following:
        #mark all ports_scanned as False
        #call the threaded_scan function with the given number of threaded_scan
        #calculate how much time it took to scan all ports using the given number of ports
        #make sure that this scan covered all ports, by counting how many elements in the ports_scanned list is True
        #print the following the number of ports checked from the previous step, the number of threads used, the time taken to do the scan. Print time in seconds with two digits after the decimal point.
            #example output: "Scanning 65535 ports using 3 thread(s): 16.93 seconds."
    #repeat this process with different number of threads as indicated in the following list
    #num_of_threads = [1, 2, 3, 4, 5, 10, 20, 30, 50, 100, 500, 1000, 2000, 5000, 10000]
    pass

if __name__ == "__main__":
    main()
