import src.set_up_proxy as set_up_proxy
import src.bot_creation as bot_creation
import src.bot_utils as bot_utils
import src.utils.page_parsing as page_parsing
from models.user_model import User
import re
import urllib
from bs4 import BeautifulSoup

set_up_proxy.set_up_proxy()
bot = bot_creation.create_bot()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Start has been fired')

@bot.message_handler(commands=['register'])
def register_routine(message):
    bot.send_message(message.chat.id, 'Registering')
    print(message.text)
    account = message.text.split(' ')[1]
    new_user = {'chat_id': str(message.chat.id),
                'account': account}
    collection.insert_one(new_user)

@bot.message_handler(content_types=['text'])
def work_with_request(message):
    message.text = message.text.lower().strip()
    try:
        if re.match(r'\d{6}', message.text):
            bot.send_message(message.chat.id, f'Searching for {message.text}')
            uf = urllib.request.urlopen(f'http://mup-kgs-simf.ru/index.php?str=nach_dolg&lschet={message.text}')
            html = uf.read()
            html = html.decode('utf-8')
            soup = BeautifulSoup(html, features='lxml')
            soup_result = soup.find('div', attrs={'class': 'print1'})
            response = soup_result.text
            bot.send_message(message.chat.id, response)

            soup_result = soup.find('div', attrs={'class': 'kvit'}).text
            result = " ".join(soup_result.split())

            response = re.search(r'По состоянию на \d\d\.\d\d\.\d\d\d\d', result).group() + '\n'

            response += re.search(r'Тариф за 1м2 с \d\d\.\d\d.\d\d\d\d=(.)*р\.', result).group() + '\n'

            response += re.search(r'Сумма к оплате (\d)*,(\d)* руб.', result).group() + '\n'

            print(response)

            bot.send_message(message.chat.id, response)
    except Exception as e:  # ignoring PeP
        print(f'{type(e)}:{e}')
        bot.send_message(message.chat.id, 'ops!')


try:
    bot.polling(none_stop=True)
except Exception as err:
    print(err)
    bot_utils.restart_bot(bot)
