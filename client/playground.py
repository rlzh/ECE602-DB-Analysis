
import socket
import json
import pickle
import threading
import time


def send_tcp_message(data, port=9999):
    # get local machine name
    host = socket.gethostname()
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    data = pickle.dumps(json.dumps(data))
    s.send(data)
    return s


def listen_to_server(s):
    while 1:
        msg = pickle.dumps("MEHMEH")
        s.send(msg)
        resp = s.recv(1024)
        if resp:
            print(pickle.loads(resp))
        time.sleep(1)


host = socket.gethostname()
port = 9999
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
listen_to_server(s)
msg = pickle.dumps("MEH")
s.send(msg)
threading.Thread(target=listen_to_server, args=(s,)).start()
msg = pickle.dumps("AHSDF")
s.send(msg)
