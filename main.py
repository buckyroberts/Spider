import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
from sys import argv,exit
from os import _exit

if len(argv) < 4:
        print ('usage: python3 ' + argv[0] + ' <project name> <base url> <no of threads>')
        exit(1)

PROJECT_NAME = argv[1]
HOMEPAGE = argv[2]
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.lst'
CRAWLED_FILE = PROJECT_NAME + '/crawled.lst'
NUMBER_OF_THREADS = int(argv[3])
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


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

try:
	create_workers()
	crawl()
except:
	print ('[!] Quiting...')
	Spider.update_files()
	_exit(0)
