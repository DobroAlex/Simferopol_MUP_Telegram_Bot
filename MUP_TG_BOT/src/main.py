import src.set_up_proxy as set_up_proxy
import src.bot_creation as bot_creation
import src.bot_utils as bot_utils
import src.utils.page_parsing as page_parsing
import src.utils.link_generator as link_generator
import src.controllers.start_message as start_message_controller
import src.controllers.register_user as register_user
import src.controllers.delete_user as delete_user
import src.controllers.account_received as acc_received
import src.utils.db_utils as db_utils
from models.user_model import User
import re
import urllib
from bs4 import BeautifulSoup

set_up_proxy.set_up_proxy()
bot = bot_creation.create_bot()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, start_message_controller.start_message())


@bot.message_handler(commands=['register'])
def register_handler(message):
    account = message.text.split(' ')[1]
    bot.send_message(message.chat.id, register_user.register_user(User, account, message.chat.id))


@bot.message_handler(commands=['delete_me'])
def delete_me_handler(message):
    bot.send_message(message.chat.id, delete_user.delete_user(User, str(message.chat.id)))


@bot.message_handler(content_types=['text'])
def work_with_request(message):
    message.text = message.text.lower().strip()
    if re.match(r'\d{6}', message.text):
        res = acc_received.account_received(message.text)
        bot.send_message(message.chat.id, acc_received.account_received(message.text))


try:
    bot.polling(none_stop=True)
except Exception as err:
    print(err)
    bot_utils.restart_bot(bot)
