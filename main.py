from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


class Parser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.handle_a(attrs)

    def error(self, message):
        print(message)

    def handle_a(self, attrs):
        for (attribute, value) in attrs:
            if attribute == 'href':
                url = parse.urljoin('https://thenewboston.com/', value)
                print(attribute + ': ' + url)


response = urlopen('https://thenewboston.com/')
htmlString = ''
if response.getheader('Content-Type') == 'text/html':
    htmlBytes = response.read()
    htmlString = htmlBytes.decode("utf-8")

parser = Parser()
parser.feed(htmlString)
