from urllib.parse import urlparse

top_level_domain= set(["com","org","net","int","edu","gov","mil"])

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        domain_name = results[-2] + '.' + results[-1]
        for x in range(len(results)-3,0,-1):
            domain_name = results[x] + '.' + domain_name
            if results[len(results)-x] not in top_level_domain:
                break
        return domain_name
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

