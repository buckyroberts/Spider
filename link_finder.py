from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    # setting up our program
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        
        # we are checking the tag name and we are using the tag if it is a ancher tag like this <a href="example.com" />
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    
                    # Example /user/form/submit is gonna become https://www.google.com/user/form/submit
                    url = parse.urljoin(self.base_url, value)
                    
                    # we are adding to the set() of links 
                    self.links.add(url)
    
    # all this module does is return the set of links to the main module
    def page_links(self):
        return self.links
    
    # this is like a try and catch for parsing our html using the HTMLParser module
    def error(self, message):
        pass
