import src.set_up_proxy as set_up_proxy
import src.bot_creation as bot_creation
import src.bot_utils as bot_utils
import src.utils.page_parsing as page_parsing
import src.utils.link_generator as link_generator
from models.user_model import User
import re
import urllib
from bs4 import BeautifulSoup

set_up_proxy.set_up_proxy()
bot = bot_creation.create_bot()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Welcome to bot. You can send your account (6 digits) to retrieve current '
                                      'information or use "/register 6digits" to get this information regularly ')


@bot.message_handler(commands=['register'])
def register_routine(message):
    account = message.text.split(' ')[1]
    if not page_parsing.is_valid_page(link_generator.generate_page_from_account(account)):
        bot.send_message(message.chat.id, 'Invalid account')
        return
    if User.objects(chat_id=str(message.chat.id)):
        bot.send_message(message.chat.id, 'Account already exists')
        return
    User(chat_id=str(message.chat.id), account=account).save()
    result_msg = f'New user {str(message.chat.id)} : {account} saved'
    bot.send_message(message.chat.id, result_msg)


@bot.message_handler(content_types=['text'])
def work_with_request(message):
    message.text = message.text.lower().strip()
    try:
        if re.match(r'\d{6}', message.text):
            if not page_parsing.is_valid_page(f'http://mup-kgs-simf.ru/index.php?str=nach_dolg&lschet={message.text}'):
                bot.send_message(message.chat.id, 'Invalid account')
                return
            else:
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
        pass


try:
    bot.polling(none_stop=True)
except Exception as err:
    print(err)
    bot_utils.restart_bot(bot)
