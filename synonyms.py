
import requests
from bs4 import BeautifulSoup as bs


def syn(var):
    url = f'https://www.thesaurus.com/browse/{var}?s=t'

    headers = {
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'
                       ' AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/53.0.2785.143 Safari/537.36')
    }

    r = requests.get(url, headers=headers, timeout=5)
    dd = {}
    if r.status_code == 200:
        soup = bs(r.text, 'html.parser')
        scripts_info = soup.find_all('script')
        for i in scripts_info:
            inside_scripts = str(i.string)
            if 'window.INITIAL_STATE' in inside_scripts:
                div = inside_scripts.replace('\"exampleSentences\"', '-7ag1-'
                                             ).replace('\"posTabs\"', '-7ag1-')
                div = div.split('-7ag1-')
                div = div[1].split(']},{')
                for i5 in div:  # перебор definition объектов
                    i5 = i5.split('\"antonyms\"')
                    i5 = i5[0].replace('{', '-7ag1-').replace('}', '-7ag1-')
                    i5 = i5.replace('[', '-7ag1-').replace(']', '-7ag1-')
                    i5 = i5.split('-7ag1-')
                    for i in i5:
                        i = i.split('\",\"')

                        for x in i:
                            if 'definition' in x:
                                flag = True
                                mean = x.split('\":\"')[1]
                                dd[mean] = []
                            elif 'term' in x and flag:
                                syn = x.split('\":\"')[1]
                                dd[mean].append(syn)
                            elif 'similarity' in x:
                                sim = x.split('\":\"')
                                if int(sim[1]) <= 49:
                                    flag = False
    if dd:
        return dd
    return None
