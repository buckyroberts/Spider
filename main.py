from spider import Spider

spider = Spider('thenewboston', 'https://thenewboston.com/')

profile_links = spider.get_page_links('https://thenewboston.com/profile.php?user=2')
spider.add_to_set('queue', profile_links)
