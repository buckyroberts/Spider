"""Multi-threaded website crawler written in Python.

Usage:
    main.py  [--flush=<boolean>]

Options:
    -h --help           Show this screen.
    --flush=<boolean>   Empty project folder prior to crawling [default: True].

"""
from docopt import docopt
import threading
import argparse
from queue import Queue
from spider import Spider
from domain import *
from general import *


args = docopt(__doc__)

PROJECT_NAME = 'example'
HOMEPAGE = 'http://twitter.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)

QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

attrs = {
    'project_name': PROJECT_NAME,
    'base_url': HOMEPAGE,
    'domain_name': DOMAIN_NAME,
    'flush': args['--flush']
}

Spider(attrs)


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
    for link in file_to_set(PROJECT_NAME + '/queue.txt'):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(PROJECT_NAME + '/queue.txt')
    if queued_links:
        number_of_links = len(queued_links)
        print('{} links in the queue'.format(number_of_links))
        create_jobs()

create_workers()
crawl()
