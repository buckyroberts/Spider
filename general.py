from urllib.request import urlopen
from link_finder import LinkFinder

# Set for faster processing, file for saving data
queued_links = set()


# Append to a file
def append_to_file(path, data):
    with open(path, "a") as file:
        file.write(data + '\n')


# get_page_links('https://thenewboston.com/', 'https://thenewboston.com/')
def get_page_links(base_url, page_url):
    response = urlopen(base_url)
    html_string = ''
    if response.getheader('Content-Type') == 'text/html':
        html_response = response.read()
        html_string = html_response.decode("utf-8")
    link_finder = LinkFinder(base_url, page_url)
    link_finder.feed(html_string)
    return link_finder.get_page_links()


# adds a set of links to the queue
def add_links_to_list(base_url, page_url):
    for url in get_page_links(base_url, page_url):
        if url not in queued_links:
            append_to_file('links/queue.txt', url)
            queued_links.add(url)


add_links_to_list('https://thenewboston.com/', 'https://thenewboston.com/')
