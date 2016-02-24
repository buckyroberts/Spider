from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

BASE_URL = 'https://thenewboston.com/'


class Parser(HTMLParser):

    def __init__(self):
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(BASE_URL, value)
                    print(attribute + ': ' + url)

    def handle_data(self, data):
        print("Data: ", data)

    def error(self, message):
        print(message)


html_string = ''
response = urlopen(BASE_URL)

if response.getheader('Content-Type') == 'text/html':
    html_response = response.read()
    html_string = html_response.decode("utf-8")

# Create a parser and feed it text
parser = Parser()
parser.feed(html_string)
