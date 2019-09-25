import src.check_internet_connection as check_internet_connection
from time import sleep


def restart_bot(bot):
    try:
        print('Restarting bot')
        print('If no exceptions will ocure in next 5 seconds -- it means that bot if fine')
        bot.polling(none_stop=True)
    except Exception as err:
        print(err)
        if not check_internet_connection.is_connected():
            print('Awaiting 5 sec to RE-check connection')
            sleep(5)
        restart_bot(bot)  # It's probably not safe in terms of stack overflow
