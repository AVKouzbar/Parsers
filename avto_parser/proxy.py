import requests
from bs4 import BeautifulSoup as bs

def proxy_lists():
    URL = 'https://free-proxy-list.net/'
    HEADERS = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = bs(response.content, 'html.parser')
    div = soup.find_all('tbody')
    tr = div[0].find_all('tr')
    for t in tr:
        ip_0 = t.find_all('td')
        ip = ip_0[0].text
        port = ip_0[1].text
        http_s = ip_0[6].text

        if http_s == 'yes':
            proxy = {'https': 'https://' + str(ip) + ':' + str(port)}
        else:
            proxy = {'http': 'https://' + str(ip) + ':' + str(port)}
        try:
            response_proxy = requests.get('https://2ip.ru', headers=HEADERS, proxies=proxy)
            soup_proxy = bs(response_proxy.content, 'html.parser')
            div_proxy = soup_proxy.find('big', attrs={'id': 'd_clip_button'}).text
            if div_proxy == ip:
                return proxy
                break
        except: pass