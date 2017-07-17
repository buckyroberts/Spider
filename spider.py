from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
import os
from re import findall

class Spider:
	project_name = ''
	base_url = ''
	domain_name = ''
	queue_file = ''
	crawled_file = ''
	email_file = ''
	regex = r"[\w]+@{1}[\w]+\.{1}[a-zA-Z.]{2,}"
	queue = set()
	crawled = set()
	email = set()

	def __init__(self, project_name, base_url, domain_name):
		Spider.project_name = project_name
		Spider.base_url = base_url
		Spider.domain_name = domain_name
		Spider.queue_file = os.path.join(Spider.project_name, 'queue.lst')
		Spider.crawled_file = os.path.join(Spider.project_name, 'crawled.lst')
		Spider.email_file = os.path.join(Spider.project_name, 'emails.lst')
		self.boot()
		self.crawl_page('First spider', Spider.base_url)

	# Creates directory and files for project on first run and starts the spider
	@staticmethod
	def boot():
		create_project_dir(Spider.project_name)
		create_data_files(Spider.project_name, Spider.base_url)
		Spider.queue = file_to_set(Spider.queue_file)
		Spider.crawled = file_to_set(Spider.crawled_file)

	# Updates user display, fills queue and updates files
	@staticmethod
	def crawl_page(thread_name, page_url):
		if page_url not in Spider.crawled:
			print(thread_name + ' now crawling ' + page_url)
			print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
			Spider.add_links_to_queue(Spider.gather_links(page_url))
			Spider.queue.remove(page_url)
			Spider.crawled.add(page_url)
			Spider.update_files()

	# Converts raw response data into readable information and checksfor proper html formatting
	@staticmethod
	def gather_links(page_url):
		html_string = ''
		try:
			response = urlopen(page_url)
			if 'text/html' in response.getheader('Content-Type'):
				html_bytes = response.read()
			html_string = html_bytes.decode("utf-8")
			Spider.find_emails(html_string)
			finder = LinkFinder(Spider.base_url, page_url)
			finder.feed(html_string)
		except Exception as e:
			print(str(e))
			return set()
		return finder.page_links()

	# Saves queue data to project files
	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			if (url in Spider.queue) or(url in Spider.crawled):
				continue
			if Spider.domain_name != get_domain_name(url):
				continue
			Spider.queue.add(url)

	@staticmethod
	def update_files():
		set_to_file(Spider.email, Spider.email_file)
		set_to_file(Spider.queue, Spider.queue_file)
		set_to_file(Spider.crawled, Spider.crawled_file)
	@staticmethod
	def find_emails(res):
		for email in findall(Spider.regex, res):
			Spider.email.add(email)
