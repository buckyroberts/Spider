from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:

    def __init__(self, project_name, base_url):
        self.project_name = project_name
        self.base_url = base_url
        self.queue = set()
        self.crawled = set()
        self.boot()

    def boot(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.queue = file_to_set(self.project_name + '/queue.txt')
        self.crawled = file_to_set(self.project_name + '/crawled.txt')

    def get_page_links(self, page_url):
        html_string = ''
        response = urlopen(page_url)
        if response.getheader('Content-Type') == 'text/html':
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
        finder = LinkFinder(self.base_url, page_url)
        finder.feed(html_string)
        return finder.page_links()

    def add_to_set(self, name, links):
        if name == 'queue':
            self.queue.update(links)
        if name == 'crawled':
            self.crawled.update(links)

    def add_links(self, page_url):
        for url in self.get_page_links(page_url):
            if url not in self.queue:
                append_to_file(self.project_name + '/queue.txt', url)
                self.queue.add(url)
