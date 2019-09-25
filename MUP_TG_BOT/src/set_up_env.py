from os.path import join, dirname, abspath
from os import environ, getcwd
from dotenv import load_dotenv

dotenv_path = join(getcwd(), '../.env')
load_dotenv(dotenv_path)

TG_TOKEN = environ.get('TG_TOKEN')
PROXY_PROTOCOL = environ.get('PROXY_PROTOCOL')
PROXY_ADDR = environ.get('PROXY_ADDR')

ENV_VAR_LIST = [TG_TOKEN, PROXY_PROTOCOL, PROXY_ADDR]


def check_TG_token():
    if not TG_TOKEN:
        raise EnvironmentError('No TG_TOKEN in env, aborting')
    print(TG_TOKEN)


def check_PROXY_vars():
    if not PROXY_PROTOCOL or not PROXY_ADDR:
        raise EnvironmentError('Some Proxy  Vars are missing, aborting')
