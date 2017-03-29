from domain import *

HOMEPAGE = input('Enter HomePage url : ')
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_PATH = 'database/queue/'
CRAWLED_PATH = 'database/crawled/'
QUEUE_FILE = QUEUE_PATH + DOMAIN_NAME + '.txt'
CRAWLED_FILE = CRAWLED_PATH + DOMAIN_NAME + '.txt'
NUMBER_OF_THREADS = 8