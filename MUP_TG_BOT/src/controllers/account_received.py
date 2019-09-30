import src.utils.page_parsing as page_parsing
import src.utils.link_generator as link_gen
import urllib
from bs4 import BeautifulSoup
import re


def account_received(account_id: str) -> str:
    try:
        check_page = link_gen.generate_page_from_account(account_id)
        if not page_parsing.is_valid_page(check_page):
            raise RuntimeError(f'{account_id} is invalid')
        html = urllib.request.urlopen(check_page).read().decode('utf-8')

        soup = BeautifulSoup(html, features='lxml')
        soup_result = soup.find('div', attrs={'class': 'print1'})

        response = soup_result.text

        soup_result = soup.find('div', attrs={'class': 'kvit'}).text
        result = " ".join(soup_result.split())

        response += '\n\n\n'

        response += re.search(r'По состоянию на \d\d\.\d\d\.\d\d\d\d', result).group() + '\n'
        response += re.search(r'Тариф за 1м2 с \d\d\.\d\d.\d\d\d\d=(.)*р\.', result).group() + '\n'
        response += re.search(r'Сумма к оплате (\d)*,(\d)* руб.', result).group() + '\n'

        return response
    except Exception as e:
        return f'{e}'
