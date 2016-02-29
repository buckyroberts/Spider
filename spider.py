from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:

    # Class variables (shared among all instances)
    project_name =  base_url = domain_name = queue_file =  crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, attrs):
        Spider.project_name = attrs['project_name']
        Spider.base_url = attrs['base_url']
        Spider.domain_name = attrs['domain_name']
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        if(attrs["flush"]):
            remove_data_files(Spider.project_name, Spider.base_url)
        self.boot()
        self.crawl_page('Initializer', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            current_queue = len(Spider.queue)
            number_crawled = len(Spider.crawled)
            print('{} crawling: {}'.format(thread_name, page_url))
            print('Queue {} | Crawled {}'.format(current_queue, number_crawled ))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html' or \
                    response.getheader('content-type') == 'text/html;charset=utf-8':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error: can not crawl webpage')
            return set()
        return finder.page_links()

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue or Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)
