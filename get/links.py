import os

# print(f"\n{os.path.basename(__file__)} loaded -----------\n")

keywords_to_remove = [
    '.pdf',
    'protection',
    'login',
    'portfolio',
    'news',
    'founder',
    'jobs',
    'investor',
    'fintech',
    'frequently',
    'insights',
    'faq',
    'mentor',
    'headliner',
]

add_keywords_to_remove = [
        'javascript',
]

# script name
loc = "get/links"

# get line numbers
from inspect import currentframe
def ln():
    """
    print line numbers with f"{ln()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno


# domain utils
import tldextract

# def domain_from_url(url):
    
#     o = tldextract.extract(url)
#     domain = f"{o.domain}.{o.suffix}".lower()
#     if 'www.' in domain:
#         domain = domain.replace('www.','')
#     return domain

def domain_name_from_url(url):
    # import tldextract
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name



def internal(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print()
        print(f"{loc}.internal #{ln()}: {url=}")

    domain_name = domain_name_from_url(url)
    if v: 
        print(f"{loc}.internal #{ln()}: domain_name: {domain_name}")
    
    set_links = set()
    dict_mailtos = {}

    links = soup.find_all('a')

    if v:
        print(f"\n{loc}.internal #{ln()}: {len(links)} links found:\n")
    for l in links:
        # if v:
        #     print(f"\n{loc}.internal #{ln()}: {l}")
            
        try:
            href = l['href']
            if v:
                print(f"{loc}.internal #{ln()}: {type(href)} {href=}")
            if not any(ele in href for ele in keywords_to_remove):

                if domain_name in href and not href.startswith('/') and not href.startswith('mailto'): # NOT if href startswith as some links will be on a different (sub)domain
                    link = href.strip()
                    set_links.add(link)
                    if v:
                        print(f"{loc}.internal #{ln()}: ADDED {link}")
                # add mailto links to separate dict
                elif domain_name in href and href.startswith('mailto'): 
                    email = href.replace('mailto:', '').strip()
                    dict_mailtos[email] = link
                    if v:
                        print(f"{loc}.internal #{ln()}: ADDED EMAIL {email} from {link}")
                else:
                    if v:
                        print(f"{loc}.internal #{ln()}: REMOVED {href} - {domain_name} not in.")

                if href.startswith('/'):
                    link = f"{url}{href.strip()}"
                    set_links.add(link)
                    if v:
                        print(f"{loc}.internal #{ln()}: ADDED {link}")
            else:
                if v:
                    print(f"{loc}.internal #{ln()}: REMOVED {href} - blacklist")
            
        except:
            if v:
                print(f"{loc}.internal #{ln()}: ------ERROR with {l}")
            continue

    set_links = set(sorted(set_links))

    dict_return = {'internal_links':set_links,'emails':dict_mailtos}

    if v:
        print(f"\n---\n{loc}.internal #{ln()}: \nRETURNED set of all INTERNAL links ({len(set_links)}):\n{set_links}.\n---\n")

    return dict_return



def all(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    keywords_to_remove = keywords_to_remove + [
        'javascript',
    ]

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\n{loc}/all #{ln()}: {url=}\n")
    
    set_links = set()

    links = soup.find_all('a')

    if v:
        print(f"\n{loc}/all #{ln()}: {len(links)} links found:\n")
    for l in links:
        if v:
            print(f"\n{loc}/all #{ln()}: {l}")
            
        try:
            href = l['href']
            if v:
                print(f"{loc}/all #{ln()}: {type(href)} {href=}")
            if not any(ele in href for ele in keywords_to_remove):

                if not href.startswith('/'):
                    link = href.strip()

                if href.startswith('/'):
                    link = f"{url}{href.strip()}"

                set_links.add(link)
                if v:
                    print(f"{loc}/all #{ln()}: +++ADDED {link}\n\n")
            else:
                print(f"{loc}/all #{ln()}: ---REMOVED {href} - blacklist\n\n")
            
        except:
            print(f"{loc}/all #{ln()}: ------ERROR with {l}\n\n")
            continue

    list_links = list(set_links)

    if v:
        print(f"\n---\n{loc}/all #{ln()}: \nRETURNED list of ALL links ({len(list_links)}):\n{list_links}.\n---\n")

    return list_links


def socials(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    from collections import namedtuple

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\n{loc}/socials #{ln()}: {url=}\n")

    social_names = [
        'twitter',
        'linkedin',
        'facebook',
        'instagram',
        'youtube',
        'medium',
        'github',
        'tiktok',
    ]
    
    socials = namedtuple('Socials', social_names)

    links = soup.find_all('a')

    for l in links:
        try:
            link = l['href']
            # if v:
            #     print(f"\n{loc}/socials #{ln()}: checking {l}")

            if ("twitter.com" in link) and ("intent" not in link) and ('share' not in link) and ("status" not in link) and ("hashtag" not in link):
                if v:
                    print(f"+++ADDED TWITTER {link}")
                socials.twitter = link

            elif ("linkedin.com" in link):
                if v:
                    print(f"+++ADDED LINKEDIN {link}")
                socials.linkedin = link

            elif ("facebook.com" in link) and ("facebook.com/share" not in link):
                if v:
                    print(f"+++ADDED FACEBOOK {link}")
                socials.facebook = link

            elif ("instagram.com" in link):
                if v:
                    print(f"+++ADDED INSTAGRAM {link}")
                socials.instagram = link

            elif ("youtube.com" in link) and ("youtube.com/watch" not in link):
                if v:
                    print(f"+++ADDED YOUTUBE {link}")
                socials.youtube = link

            elif ("medium.com" in link):
                if v:
                    print(f"+++ADDED MEDIUM {link}")
                socials.medium = link

            elif ("github.com" in link):
                if v:
                    print(f"+++ADDED GITHUB {link}")
                socials.github = link

            elif ('tiktok.com'  in link) and ('video' not in link):
                if v:
                    print(f"+++ADDED TIKTOK {link}")
                socials.tiktok = link
            
            # x = person(first='Nic', last='Deville')
        except:
            if v:
                print(f"\n{loc}/socials #{ln()}: ------ERROR with {l}\n")
            continue

    # Cleanup: None where no value

    if not isinstance(socials.twitter, str):
        socials.twitter = None
    if not isinstance(socials.linkedin, str):
        socials.linkedin = None
    if not isinstance(socials.facebook, str):
        socials.facebook = None
    if not isinstance(socials.instagram, str):
        socials.instagram = None
    if not isinstance(socials.youtube, str):
        socials.youtube = None
    if not isinstance(socials.medium, str):
        socials.medium = None
    if not isinstance(socials.github, str):
        socials.github = None
    if not isinstance(socials.tiktok, str):
        socials.tiktok = None

    if v:
        print(f"\n---\n{loc}/socials #{ln()}: NOTE: returns namedtuple of SOCIAL links: {','.join(social_names)}.\n---\n")

    return socials


def files(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    keywords_to_remove = keywords_to_remove + [
        'javascript',
    ]

    file_extensions = (
        '.pdf',
        '.doc',
        '.docx',
        '.xls',
        '.xlsx',
        '.ppt',
        '.pptx',
        '.txt',
        '.csv',
        '.zip',
        '.rar',
        '.7z',
        '.tar',
        '.gz',
        '.tgz',
    )

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\nget.links #{ln()}: {url=}\n")
    
    set_links = set()

    links = soup.find_all('a')

    # links_files = [x['href'] for x in links if x['href'].endswith(file_extensions)]
    # if v:
    #     print(f"\n{len(links_files)} file links found:\n")
    #     for lf in links_files:
    #         print(f"{lf}")
    #     print()

    for l in links:
        # if v:
        #     print(f"\n#{ln()}: {l}")
            
        try:
            href = l['href']

            if href.endswith(file_extensions):
                if not any(ele in href for ele in keywords_to_remove):
                    if not href.startswith('/'):
                        link = href.strip()

                    if href.startswith('/'):
                        link = f"{url}{href.strip()}"

                    set_links.add(link)
                    if v:
                        print(f"+++ADDED {link}\n\n")
                else:
                    print(f"---REMOVED {href} - blacklist\n\n")
            else:
                print(f"---REMOVED {href} - wrong extension\n\n")
            
        except:
            print(f"------ERROR with {l}\n\n")
            continue

    list_links = list(set_links)

    if v:
        print(f"\n---\n{loc}/files #{ln()}: \nRETURNED list of all FILES links ({len(list_links)}):\n{list_links}.\n---\n")

    return list_links

########################################################################################################

if __name__ == '__main__':

    url = "https://www.balderton.com/"

    from get.soup import main as get_soup_tuple

    soup_tuple = get_soup_tuple(url)
    # soup = soup_tuple.soup
    # url = soup_tuple.url

    links = all(soup_tuple)

    print(f"\nlinks returned:\n")
    for link in links:
        print(link)
        print()

    # print()
    # print()
    # print('-------------------------------')
    # print(f"{os.path.basename(__file__)}")
    # print()
    # print(f"{count=}")
    # print()
    # print('-------------------------------')
    # run_time = round((time.time() - start_time), 1)
    # if run_time > 60:
    #     print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    # else:
    #     print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    # print()