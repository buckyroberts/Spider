from urllib.parse import urlparse
from tld import get_tld


# Get domain name (example.com)
def get_domain_name(url):
	# Use tld to resovle the top-level-domain

    return get_tld(url)


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


