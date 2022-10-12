from bs4 import BeautifulSoup
from urllib import parse

class LinkFinder() :
    def __init__(self , response , base_url) :
        self.soup  = BeautifulSoup(response.text , 'html.parser')
        self.links = set()
        self.base_url = base_url
    def find_links(self) :
        for link in self.soup.find_all('a' ,href=True) :
            url = parse.urljoin(self.base_url ,link['href'])
            self.links.add(url)

    def page_links(self):
        return self.links
