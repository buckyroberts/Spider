from spider import Spider

PROJECT_NAME = 'thenewboston'
HOMEPAGE = 'https://thenewboston.com/'


def start():
    spider = Spider(PROJECT_NAME, HOMEPAGE)
    spider.crawl_page(HOMEPAGE)

start()
