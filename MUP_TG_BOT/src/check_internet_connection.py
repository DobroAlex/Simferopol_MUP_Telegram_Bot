import socket

REMOTE_SERV: str = 'www.google.com'


def is_connected(hostname=REMOTE_SERV):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 5)
        s.close()
        return True
    except:  # ignoring PEP
        print('No Internet connection')
        pass
    return False
