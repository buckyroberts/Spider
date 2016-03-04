"""
    Usage: python3 main.py [-h] [-wk] -u <homepage> [-p <project folder>] [-j <number of threads>]

    Examples:
        python3 main.py -p ../thenewboston -u https://thenewboston.com      # Specified project folder
        python3 main.py -u https://thenewboston.com                       	# Creates project folder thenewboston.com
        python3 main.py -w -u https://thenewboston.com                      # start fresh (wipe existing files)
        python3 main.py -k -u https://thenewboston.com                      # keep the data
        python3 main.py -wk -u https://thenewboston.com -j20                # 20 threads
        python3 main.py -h                                                  # Displays usage

"""

import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import getopt, sys
import signal


PROJECT_NAME = ''
HOMEPAGE = ''
DOMAIN_NAME = ''
QUEUE_FILE = ''
CRAWLED_FILE = ''
NUMBER_OF_THREADS = 8
keep = False
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


# Cleanup and quit
def quit_gracefully(signal=None, frame=None):
	print("\nQuitting.")
	with queue.mutex: queue.queue.clear()
	if not keep:
		try:
			delete_file_contents(QUEUE_FILE)
		except:
			pass
	sys.exit(0)

# Enable process termination
def register_signal_handler():
	signal.signal(signal.SIGINT, quit_gracefully)
	signal.signal(signal.SIGTERM, quit_gracefully)


# Print short usage and exit
def usage():
	print('Usage: ' + sys.argv[0] + ' [-h] [-wk] -u <homepage> [-p <project folder>] [-j <number of threads>]')
	sys.exit()

# Print detailed usage and exit
def detailed_usage():
	print('\nUsage: ' + sys.argv[0] + ' [-h] [-wk] -u <homepage> [-p <project folder>] [-j <number of threads>]\n')
	print('Options:')
	print('-h\t\tDisplays this help')
	print('-w\t\tWipe existing files (start fresh)')
	print('-k\t\tKeep the queue file contents (continue crawling at a different time)')
	print('-u <url>\tThe homepage/starting point')
	print('-p <project>\tSpecify a specific output folder')
	print('-j <number>\tSpecify number of crawling threads. Default 8\n')
	sys.exit()

# Set constants to values provided by command line
def options():
	global PROJECT_NAME
	global HOMEPAGE
	global NUMBER_OF_THREADS
	global DOMAIN_NAME
	global QUEUE_FILE
	global CRAWLED_FILE
	global keep
	wipe = False
	opts = None
	args = None
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hwkp:u:j:')
	except getopt.GetoptError as e:
		print(str(e))
		usage()

	if len(args) != 0:
		usage()

	for opt, val in opts:
		if opt == '-h':
			detailed_usage()
		elif opt == '-w':
			wipe = True
		elif opt == '-p':
			PROJECT_NAME = val
		elif opt == '-u':
			HOMEPAGE = val
		elif opt == '-k':
			keep = True
		elif opt == '-j':
			try:
				NUMBER_OF_THREADS = int(val)
			except:
				print('Value for option -j should be an integer.')
				usage()




	if HOMEPAGE == '':
		usage()

	if NUMBER_OF_THREADS <= 0:
		print('Value for option -j should be greater than 0.')
		usage()

	if PROJECT_NAME == '':
		PROJECT_NAME = get_domain_name(HOMEPAGE)


	DOMAIN_NAME = get_domain_name(HOMEPAGE)

	if DOMAIN_NAME == '':
		usage()

	QUEUE_FILE = PROJECT_NAME + '/queue.txt'
	CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'

	if wipe:
		try:
			delete_file_contents(QUEUE_FILE)
		except:
			pass

		try:
			delete_file_contents(CRAWLED_FILE)
		except:
			pass


def main():
	register_signal_handler()
	options()
	Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
	create_workers()
	crawl()



if __name__ == '__main__':
	main()





