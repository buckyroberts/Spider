from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    # it initializes or constructs before the actual code in this runs
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    
    def page_links(self):
        return self.links
    
    #when error occurs it displays where error occured with a message 
    def error(self, message):
        pass
