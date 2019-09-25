import set_up_env
import telebot


def create_bot():
    set_up_env.check_TG_token()
    return telebot.TeleBot(set_up_env.TG_TOKEN)
