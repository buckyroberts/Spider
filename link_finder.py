from urlparse import urljoin
from formatter import DumbWriter,AbstractFormatter
from htmllib import HTMLParser
from cStringIO import StringIO
from string import find

class LinkFinder(object):

    def __init__(self,base_url,page_url):
        self.base_url = base_url
        self.page_url = page_url

    def parseAndGetLinks(self,html_string):
        try:
            self.parser = HTMLParser(AbstractFormatter(DumbWriter(StringIO())))
            self.parser.feed(html_string)
            self.parser.close()
            links = []
            for eachLink in self.parser.anchorlist:
                if eachLink[:4] != "http" and find(eachLink, "://") == -1:
                    eachLink = urljoin(self.base_url, eachLink)
                links.append(eachLink)
            return links
        except IOError:
            return []