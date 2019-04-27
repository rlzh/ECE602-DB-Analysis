import socket
import pickle
import json
import time
import random
import traceback
import threading
import sys
import datamining as datamining
import datacleaning
import argparse
import getpass
import shared
import pymysql
import os

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

# parse args
PARSER = argparse.ArgumentParser(description="")
PARSER.add_argument('-u', '--user', default='root',
                    help='username for database access')
PARSER.add_argument('-p', '--password', action='store_true', dest='password',
                    help='password for database access')
PARSER.add_argument('-pt', '--port', default=9999, type=int,
                    help='port server should listen on for incoming client connection & messages')
PARSER.add_argument('-db', '--database', default='lahman2016',
                    help='name of database that should be used')
PARSER.add_argument('-ht', '--host', default='localhost',
                    help='host name for database access')
ARGS = PARSER.parse_args()
print(ARGS)

# set shareds
if ARGS.password:
    shared.password = getpass.getpass()
shared.database = ARGS.database
shared.user = ARGS.user
shared.host = ARGS.host


def handle_message(msg):
    try:
        msg = json.loads(msg)
        msg_type = msg[MSG_TYPE_KEY]
        resp = {
            STATUS_KEY: OK_STR,
            MSG_TYPE_KEY: msg[MSG_TYPE_KEY],
        }
        if msg_type == CLEAN_MSG_TYPE:
            ok = datacleaning.handle_clean(msg[DATA_KEY])
            resp[STATUS_KEY] = OK_STR if ok else ERR_STR
        elif msg_type == UNCLEAN_MSG_TYPE:
            ok = datacleaning.handle_unclean()
            resp[STATUS_KEY] = OK_STR if ok else ERR_STR
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

            acc, f1 = datamining.AnalyzeMining(mode, table)

            mining_data = {
                "acc": acc,
                "f1_score": f1
            }
            resp[DATA_KEY] = mining_data

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
    except Exception as e:
        traceback.print_exc()
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

def main(argv):

    # when start create view first
    host = shared.host
    user = shared.user
    password = shared.password
    database = shared.database

    db = pymysql.connect(host,user,password,database)
    print("connecting to db..")

    # prepare a cursor object using cursor() method
    c = db.cursor()

    # Execute the SQL command
    fd = open(os.path.join(shared.abs_path,'createview.sql'), 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            if len(command) > 0:
                c.execute(command)
        except Exception as e:
            print("Error executing command")
    # disconnect from server
    db.close()
    print("disconnecting from db..")

    # to do: when exit drop view
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()
    port = ARGS.port

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
    main(sys.argv[1:])
