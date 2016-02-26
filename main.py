from spider import Spider

spider = Spider('thenewboston', 'https://thenewboston.com/')

print('\n----- Queue (' + str(len(spider.queue)) + ') -----')
for item in spider.queue:
    print(item)

print('\n----- Crawled (' + str(len(spider.crawled)) + ') -----')
for item in spider.crawled:
    print(item)
