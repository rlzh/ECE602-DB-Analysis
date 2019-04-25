import socket
import pickle
import json
import time
import random
import traceback
import threading

import datamining

# shared network message definitions
BUFFER_SIZE = 1024
MSG_TYPE_KEY = "t"
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
    try:
        msg = json.loads(msg)
        msg_type = msg[MSG_TYPE_KEY]
        resp = {
            STATUS_KEY: OK_STR,
            MSG_TYPE_KEY: msg[MSG_TYPE_KEY],
        }
        # dummy sleep
        time.sleep(1)
        if msg_type == CLEAN_MSG_TYPE:
            pass
            # todo: call clean func here
            # e.g. resp["d"], success = clean_func()
        elif msg_type == UNCLEAN_MSG_TYPE:
            pass
            # todo: call clean func here
            # e.g. resp["d"], success = clean_func()
        elif msg_type == ANALYZE_MSG_TYPE:

            content = msg[DATA_KEY]
            table = content[TABLES_KEY]
            mode = content[ANALYZE_MODE_KEY]

            if mode == "HoF Nomination":
                mode = "nom"
            elif mode == "HoF Entry":
                mode = "hof"
            elif mode == "Player-to-Manager":
                mode = "man"

            if table[0] == "Batting":
                table = "Batting"
            elif table[0] == "Fielding":
                table = "Fielding"
            elif table[0] == "Pitching":
                table = "Pitching"
            else:
                table = "All"

            acc,f1 = datamining.AnalyzeMining(mode, table)

            mining_data = {
                "acc": acc,
                "f1_score": f1
            }
            resp[DATA_KEY] = mining_data

            # todo: call analyze func here
            # e.g. resp["d"], success = analyze_func()

        elif msg_type == VALIDATE_MSG_TYPE:
            # dummy resp (comment out later)
            # Received msg: {"t": "val", "d": {"ayz_m": "HoF Nomination", "fn": "ww ", "ln": "aa"}}
            content = msg[DATA_KEY]
            mode = content[ANALYZE_MODE_KEY]
            fn = content[FIRST_NAME_KEY]
            ln = content[LAST_NAME_KEY]

            if mode == "HoF Nomination":
                mode = "nom"
            elif mode == "HoF Entry":
                mode = "hof"
            elif mode == "Player-to-Manager":
                mode = "man"

            pred, real = datamining.ValidationMining(mode, fn, ln)

            mining_data = {
                "predict": pred,
                "gnd truth": real
            }
            resp[DATA_KEY] = mining_data

            # todo: call analyze func here
            # e.g. resp["d"], success = validate_func()
    except Exception as e:
        return {STATUS_KEY: ERR_STR}
    return resp


def listen_to_client(s):
    try:
        while 1:
            msg = s.recv(BUFFER_SIZE)
            msg = pickle.loads(msg)
            print("Received msg: " + str(msg))
            resp = handle_message(msg)
            print("Sending resp: " + str(resp))
            s.send(pickle.dumps(json.dumps(resp)))
    except Exception as e:
        # traceback.print_exc()
        s.close()


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
            threading.Thread(target=listen_to_client,
                             args=(clientsocket,)).start()
        except Exception as e:
            traceback.print_exc()
            continue


if __name__ == '__main__':
    main()
