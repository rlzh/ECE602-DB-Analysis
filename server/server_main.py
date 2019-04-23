import socket
import pickle
import json
import time
import random
import traceback

# shared network message definitions
BUFFER_SIZE = 1024
TYPE_KEY = "t"
STATUS_KEY = "s"
DATA_KEY = "d"
OK_STR = "ok"
ERR_STR = "err"
CLEAN_MSG_TYPE = "cln"
UNCLEAN_MSG_TYPE = "ucln"
ANALYZE_MSG_TYPE = "ayz"
VALIDATE_MSG_TYPE = "val"
TABLES_KEY = "tbl"
ANALYZE_MODE_KEY = "ayz_m"
FIRST_NAME_KEY = "fn"
LAST_NAME_KEY = "ln"


def handle_message(msg):
    print(type(msg))
    print(msg)
    msg = json.loads(msg)
    resp = {STATUS_KEY: OK_STR}
    time.sleep(1)
    msg_type = msg[TYPE_KEY]
    if msg_type == CLEAN_MSG_TYPE:
        pass
        # todo: call clean func here
        # e.g. resp["d"], success = clean_func()
    elif msg_type == UNCLEAN_MSG_TYPE:
        pass
        # todo: call clean func here
        # e.g. resp["d"], success = clean_func()
    elif msg_type == ANALYZE_MSG_TYPE:
        # dummy resp (comment out later)
        dummy_data = {
            "acc": random.randint(80, 95),
            "precision": random.randint(57, 83)
        }
        resp[DATA_KEY] = dummy_data

        # todo: call analyze func here
        # e.g. resp["d"], success = analyze_func()

    elif msg_type == VALIDATE_MSG_TYPE:
        # dummy resp (comment out later)
        dummy_data = {
            "predict": "yes" if random.randint(1, 2) == 2 else "no",
            "gnd truth": "yes" if random.randint(1, 2) == 2 else "no"
        }
        resp[DATA_KEY] = dummy_data

        # todo: call analyze func here
        # e.g. resp["d"], success = validate_func()

    return resp


def main():
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()
    port = 9999

    # bind to the port
    serversocket.bind((host, port))

    # queue up to 5 requests
    serversocket.listen(5)
    clientsocket = None
    while True:
        # establish a connection
        print("Listening for client connection on {}:{}...".format(host, port))
        clientsocket, addr = serversocket.accept()
        try:
            print("Got a connection from %s" % str(addr))
            msg = clientsocket.recv(BUFFER_SIZE)
            msg = pickle.loads(msg)
            print("Received msg: " + str(msg))
            resp = handle_message(msg)
            print("Sending resp: " + str(resp))
            clientsocket.send(pickle.dumps(json.dumps(resp)))
            clientsocket.close()
        except Exception as e:
            traceback.print_exc()
            continue


if __name__ == '__main__':
    main()
