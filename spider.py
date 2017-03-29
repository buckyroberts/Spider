from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    queue = set()
    crawled = set()

    def __init__(self):
        self.boot()
        self.crawl_page('First spider', HOMEPAGE)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_data_files()
        Spider.queue = file_to_set(QUEUE_FILE)
        Spider.crawled = file_to_set(CRAWLED_FILE)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getcode() == 200 and 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(HOMEPAGE, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if DOMAIN_NAME != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, QUEUE_FILE)
        set_to_file(Spider.crawled, CRAWLED_FILE)
