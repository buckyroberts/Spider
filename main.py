"""
    Usage: python3 main.py [-h] -p <project name> -u <homepage> [-j <number of threads>]

    Examples:
        python3 main.py -p thenewboston -u https://thenewboston.com
        python3 main.py -p thenewboston -u https://thenewboston.com -j20    # 20 threads
        python3 main.py -h  # Displays usage

"""

import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import getopt, sys


PROJECT_NAME = ''
HOMEPAGE = ''
DOMAIN_NAME = ''
QUEUE_FILE = ''
CRAWLED_FILE = ''
NUMBER_OF_THREADS = 8
queue = Queue()



# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


# Print usage and exit
def usage():
    print('Usage: ' + sys.argv[0] + ' [-h] -p <project name> -u <homepage> [-j <number of threads>]')
    sys.exit()

# Set constants to values provided by command line
def options():
    global PROJECT_NAME
    global HOMEPAGE
    global NUMBER_OF_THREADS
    global DOMAIN_NAME
    global QUEUE_FILE
    global CRAWLED_FILE
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:u:j:')
    except getopt.GetoptError as e:
        print(str(e))
        usage()

    if len(args) != 0:
        usage()

    for opt, val in opts:
        if opt == '-h':
            usage()
        elif opt == '-p':
            PROJECT_NAME = val
        elif opt == '-u':
            HOMEPAGE = val
        elif opt == '-j':
            try:
                NUMBER_OF_THREADS = int(val)
            except:
                print('Value for option -j should be an integer.')
                usage()

    if HOMEPAGE == '' or PROJECT_NAME == '':
        usage()

    DOMAIN_NAME = get_domain_name(HOMEPAGE)

    if DOMAIN_NAME == '':
        usage()

    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'

   



        


def main():
    options()
    Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
    create_workers()
    crawl()



if __name__ == '__main__':
    main()




