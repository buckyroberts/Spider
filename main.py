from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

BASE_URL = 'https://thenewboston.com/'
links = set()


class LinkFinder(HTMLParser):

    def __init__(self):
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(BASE_URL, value)
                    links.add(url)

    def error(self, message):
        pass


html_string = ''
response = urlopen(BASE_URL)

if response.getheader('Content-Type') == 'text/html':
    html_response = response.read()
    html_string = html_response.decode("utf-8")

link_finder = LinkFinder()
link_finder.feed(html_string)

for link in links:
    print(link)
