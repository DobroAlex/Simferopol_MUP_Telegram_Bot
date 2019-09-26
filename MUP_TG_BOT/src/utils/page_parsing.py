from bs4 import BeautifulSoup
import urllib


def is_valid_page(addr):
    content = urllib.request.urlopen(addr).read().decode('utf-8')
    soup = BeautifulSoup(content, features='lxml')
    soup_result = soup.find('div', attrs={'class': 'nachislenija_div'})
    if 'Вы неточно ввели' in soup_result.text:
        return False
    return True
