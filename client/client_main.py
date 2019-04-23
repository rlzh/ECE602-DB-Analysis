import socket
import pickle
import json
import traceback
import tkinter as tk
import threading
import time

from tkinter import *
from tkinter import scrolledtext

BUTTON_WIDTH = 15
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


class Window(Frame):

    def __init__(self, title, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.title = title
        self.first_name_str = StringVar()
        self.last_name_str = StringVar()
        self.clean_str = StringVar()
        self.clean_str.set("Clean")
        self.analysis_mode_int = IntVar()
        self.analysis_mode_int.set(0)
        self.serversocket = None
        self.request_buttons = []
        self.clean_options_labels = [
            "Missing SchoolIDs",
            "Missing PlayerIDs",
            "Missing TeamIDs",
            "Add Indices",
        ]
        self.query_table_labels = [
            "Batting",
            "BattingPost",
            "Fielding",
            "FieldingPost",
            "Pitching",
            "PitchingPost",
        ]
        self.analysis_mode_labels = [
            "HoF Nomination",
            "HoF Entry",
            "Player-to-Manager",
        ]
        self.init_window()
        self.init_socket()

    def init_window(self):
        # changing the title of our master widget
        self.master.title(self.title)

        # cleaning layout setup
        self.clean_frame = tk.LabelFrame(self.master, text="Data Cleaning")
        self.clean_frame.pack(fill="both", expand="yes")
        # cleaning options
        self.clean_options_frame = tk.LabelFrame(
            self.clean_frame, text="Cleaning Options")
        self.clean_options_frame.pack(side="left", expand="yes")
        self.clean_checkboxes = []
        self.clean_checkbox_ints = []
        for label in self.clean_options_labels:
            chk_state = IntVar()
            chk_state.set(1)
            chk = Checkbutton(self.clean_options_frame, text=label,
                              variable=chk_state, anchor='w')
            chk.pack(side='bottom')
            self.clean_checkboxes.append(chk)
            self.clean_checkbox_ints.append(chk_state)
        # clean button
        clean_button = tk.Button(
            self.clean_frame,
            textvariable=self.clean_str,
            width=BUTTON_WIDTH,
            command=self.clean_unclean,
        )
        clean_button.pack(side="right")
        self.request_buttons.append(clean_button)

        # analysis layout setup
        analysis_frame = tk.LabelFrame(self.master, text="Data Analysis")
        analysis_frame.pack(fill="both", expand="yes")
        # analysis options frame
        analysis_options_frame = tk.LabelFrame(
            analysis_frame, text="Analysis Options")
        analysis_options_frame.pack(side="left", expand="yes")
        self.analyze_listbox = tk.Listbox(analysis_options_frame,
                                          selectmode="multiple")
        self.analyze_listbox.pack(side='left', expand='yes')
        # add each query table to listbox
        for i in range(len(self.query_table_labels)):
            self.analyze_listbox.insert(i, self.query_table_labels[i])
        # analysis type frame
        analysis_type_frame = tk.LabelFrame(
            analysis_frame, text="Analysis Type")
        analysis_type_frame.pack(side='left', expand='yes')
        self.analysis_radiobuttons = []
        for i in range(len(self.analysis_mode_labels)):
            r = tk.Radiobutton(analysis_type_frame,
                               text=self.analysis_mode_labels[i],
                               variable=self.analysis_mode_int,
                               value=i,
                               anchor='w')
            r.pack()
            self.analysis_radiobuttons.append(r)
        analyze_button = tk.Button(
            analysis_frame,
            text="Analyze",
            width=BUTTON_WIDTH,
            command=self.analyze,
        )
        analyze_button.pack(side="right")
        self.request_buttons.append(analyze_button)

        # validate layout setup
        validation_frame = tk.LabelFrame(
            self.master, text="Data Validation")
        validation_frame.pack(fill="both", expand="yes")
        first_name_label = tk.Label(
            validation_frame, text="First Name")
        first_name_label.pack(side="left")
        first_name_entry = tk.Entry(
            validation_frame, textvariable=self.first_name_str)
        first_name_entry.pack(side="left")
        last_name_label = tk.Label(
            validation_frame, text="Last Name")
        last_name_label.pack(side="left")
        last_name_entry = tk.Entry(
            validation_frame, textvariable=self.last_name_str)
        last_name_entry.pack(side="left")
        validate_button = tk.Button(
            validation_frame,
            text="Validate",
            width=BUTTON_WIDTH,
            command=self.validate,
        )
        validate_button.pack(side="right")
        self.request_buttons.append(validate_button)

        # output log layout setup
        output_frame = tk.LabelFrame(self.master, text="Output Log")
        output_frame.pack(fill="x")
        self.console = scrolledtext.ScrolledText(output_frame)
        self.console.pack(fill="x")
        self.console.config(height=10)

        # bottom buttons
        bot_frame = tk.Frame(self.master)
        bot_frame.pack(fill="both", expand="yes", side="bottom")
        clear_button = tk.Button(
            bot_frame,
            text="Clear",
            width=BUTTON_WIDTH,
            command=self.clear_console,
        )
        clear_button.pack(side="left")
        self.cancel_button = tk.Button(
            bot_frame,
            text="Cancel",
            width=BUTTON_WIDTH,
            command=self.cancel_request,
        )
        # self.cancel_button.pack(side="right")
        self.cancel_button.config(state="disabled")

    def init_socket(self):
        if self.serversocket != None:
            self.serversocket.close()
        try:
            host = socket.gethostname()
            port = 9999
            # create a socket object
            self.serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.connect((host, port))
            self.log("Connected to server!")
        except Exception as e:
            self.log("CLANG! error while connecting to server")

    def clean_unclean(self):
        '''
        Method that toggles between sending clean & unclean request to server
        '''
        msg = {
            MSG_TYPE_KEY: "",
        }
        if self.clean_str.get() == "Clean":
            msg[MSG_TYPE_KEY] = UNCLEAN_MSG_TYPE
        else:
            msg[MSG_TYPE_KEY] = CLEAN_MSG_TYPE
            # gather options from checkboxes
            bool_list = {}
            for labels, state in list(zip(self.clean_options_labels, self.clean_checkbox_ints)):
                bool_list[labels] = state.get()
            msg[DATA_KEY] = bool_list
        self.send_request(msg)

    def analyze(self):
        # send analyze request to server
        msg = {
            MSG_TYPE_KEY: ANALYZE_MSG_TYPE,
        }
        table_list = []
        for i in self.analyze_listbox.curselection():
            table_list.append(self.query_table_labels[i])
        if len(table_list) == 0:
            self.log("CLANG! need to select at least one table for analysis")
            return
        analysis_mode = self.analysis_mode_labels[self.analysis_mode_int.get()]
        data = {
            TABLES_KEY: table_list,
            ANALYZE_MODE_KEY: analysis_mode,
        }
        msg[DATA_KEY] = data
        self.send_request(msg)
        return

    def validate(self):
        # send validate request to server
        msg = {
            MSG_TYPE_KEY: ANALYZE_MSG_TYPE,
        }
        analysis_mode = self.analysis_mode_labels[self.analysis_mode_int.get()]
        data = {
            ANALYZE_MODE_KEY: analysis_mode,
            FIRST_NAME_KEY: self.first_name_str.get(),
            LAST_NAME_KEY: self.last_name_str.get(),
        }
        msg[DATA_KEY] = data
        self.send_request(msg)
        return

    def log(self, msg):
        '''
        Logs msg onto console frame 
        msg - string to be logged
        '''
        self.console.insert(tk.INSERT, "{}\n".format(msg))

    def clear_console(self):
        '''
        Clears all content from console frame
        '''
        self.console.delete(1.0, tk.END)

    def update_request_button_state(self, state):
        '''
        Updates the state of all buttons that send requests to the server
        state - 'disabled', 'active', 'normal' 
        '''
        for button in self.request_buttons:
            button.config(state=state)

    def send_request(self, msg):
        if self.serversocket == None or self.serversocket.fileno == -1:
            self.init_socket()
            return
        try:
            # disable request buttons
            self.update_request_button_state("disabled")
            # enable cancel request button
            self.cancel_button.config(state="normal")
            self.log("Sending request <{}>...".format(msg[MSG_TYPE_KEY]))
            self.serversocket.send(pickle.dumps(json.dumps(msg)))
            threading.Thread(target=self.listen_to_server,
                             args=(msg[MSG_TYPE_KEY],)).start()
        except Exception as e:
            traceback.print_exc()
            self.log("CLANG! error while sending request.")
            if self.serversocket != None:
                self.serversocket.close()
            # enable request buttons
            self.update_request_button_state("normal")
            # disable cancel request button
            self.cancel_button.config(state="disabled")

    def listen_to_server(self, message_type):
        self.log("Awaiting response <{}>...".format(message_type))
        resp = self.serversocket.recv(BUFFER_SIZE)
        resp = json.loads(pickle.loads(resp))
        # disable cancel request button
        self.cancel_button.config(state="disabled")
        # enable request buttons
        self.update_request_button_state("normal")
        # log results to output
        self.log("Server reponse status: {}".format(resp[STATUS_KEY]))
        if resp[STATUS_KEY] == OK_STR and DATA_KEY in resp:
            self.log("{} result: ".format(resp[DATA_KEY]))
            # toggle clean/unclean button text
            if resp[MSG_TYPE_KEY] == CLEAN_MSG_TYPE:
                self.clean_str.set("Unclean")
            elif resp[MSG_TYPE_KEY] == UNCLEAN_MSG_TYPE:
                self.clean_str.set("Clean")

    # unused func
    def cancel_request(self):
        if self.serversocket == None:
            return
        # self.serversocket.close()
        # self.serversocket = None
        # disable cancel request button
        # self.cancel_button.config(state="disabled")
        # enable request buttons
        # update_request_button_state("normal")
        # self.log("Request canceled")


def main():
    root = Tk()

    # size of the window
    root.geometry("700x600")

    app = Window("ECE656 Project", root)
    root.mainloop()


if __name__ == "__main__":
    main()
