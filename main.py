import threading
import gc
import time
import mysql.connector
import mysql.connector.errors
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'crawler'
HOMEPAGE = 'https://www.whitepages.com.au/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 6
queue = Queue()
mydb = mysql.connector.connect(
  host="DBHOST",
  user="DBUSERNAME",
  passwd="DBPASSWORD",
  database="DBDATABASE"
)
mycursor = mydb.cursor()
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
        crawls = Spider.crawl_page(threading.current_thread().name, url)
        # Change the table and column to reflect your database
        sql = "INSERT INTO links (urlink) VALUES (%s)"
        val = (crawls,)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            queue.task_done()
            gc.collect()
        except (mydb.Error, mydb.Warning) as e:
            print(e)
            return None


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
        time.sleep(.500)
    queue.join()
    time.sleep(.500)
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
gc.collect()
time.sleep(.500)


