from tld import get_tld     #tld(top level domain)pakage used


def get_domain_name(url):          
    try:
        info = get_tld(url, as_object=True)
        return info.fld                         #returning domain.com
    except ValueError:
        message = "Oops! Something went wrong."
        return message                                #returning message if input is wrong
                              

def get_subdomain_name(url):
    try:
        info = get_tld(url, as_object=True)
        return info.parsed_url[1]                  #returning subdomain.domain.suffix
    except ValueError:
        message = "Oops! Something went wrong."
        return message                                  #returning message if input is wrong
