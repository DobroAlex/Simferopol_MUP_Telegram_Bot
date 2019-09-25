from telebot import apihelper
import src.set_up_env as env


def set_up_proxy():
    print(env.PROXY_PROTOCOL, env.PROXY_ADDR)
    apihelper.proxy = {env.PROXY_PROTOCOL: env.PROXY_ADDR}
