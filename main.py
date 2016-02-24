from urllib.request import urlopen
from link_finder import LinkFinder


def get_page_links(base_url, page_url):
    response = urlopen(base_url)
    html_string = ''
    if response.getheader('Content-Type') == 'text/html':
        html_response = response.read()
        html_string = html_response.decode("utf-8")
    link_finder = LinkFinder(base_url, page_url)
    link_finder.feed(html_string)
    return link_finder.get_page_links()

for link in get_page_links('https://thenewboston.com/', 'https://thenewboston.com/'):
    print(link)
