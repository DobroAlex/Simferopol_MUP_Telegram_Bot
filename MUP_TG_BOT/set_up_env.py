from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TG_TOKEN = environ.get('TG_TOKEN')
PROXY_PROTOCOL = environ.get('PROXY_PROTOCOL')
PROXY_ADDR = environ.get('PROXY_ADDR')

def check_TG_token():
    if not TG_TOKEN:
        raise EnvironmentError('No TG_TOKEN in env, aborting')
    print(TG_TOKEN)
