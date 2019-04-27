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
        self.is_clean = False
        self.analysis_mode_int = IntVar()
        self.analysis_mode_int.set(0)
        self.serversocket = None
        self.request_buttons = []
        self.clean_options_labels = [
            "Add Primary Only",
            "Add Primary and Foreign",
            "Mismatching Values",
            "All",
        ]
        self.query_table_labels = [
            "Batting",
            "Fielding",
            "Pitching",
            "All",
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
        self.clean_listbox = tk.Listbox(self.clean_options_frame,
                                          selectmode="SINGLE")
        self.clean_listbox.pack(side='left', expand='yes')
        # add each clean option to listbox
        for i in range(len(self.clean_options_labels)):
            self.clean_listbox.insert(i, self.clean_options_labels[i])
        self.clean_listbox.activate(len(self.clean_options_labels)-1)

        # clean button
        self.clean_button = tk.Button(
            self.clean_frame,
            textvariable=self.clean_str,
            width=BUTTON_WIDTH,
            command=self.clean_unclean,
        )
        self.clean_button.pack(side="right")
        self.request_buttons.append(self.clean_button)

        # analysis layout setup
        analysis_frame = tk.LabelFrame(self.master, text="Data Analysis")
        analysis_frame.pack(fill="both", expand="yes")
        # analysis options frame
        analysis_options_frame = tk.LabelFrame(
            analysis_frame, text="Analysis Options")
        analysis_options_frame.pack(side="left", expand="yes")
        self.analyze_listbox = tk.Listbox(analysis_options_frame,
                                          selectmode="SINGLE")
        self.analyze_listbox.pack(side='left', expand='yes')
        # add each query table to listbox
        for i in range(len(self.query_table_labels)):
            self.analyze_listbox.insert(i, self.query_table_labels[i])
        self.analyze_listbox.activate(len(self.query_table_labels)-1)

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
        analyze_button.config(state="disabled")
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
        validate_button.config(state="disabled")
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
            text="Clear Log",
            width=BUTTON_WIDTH,
            command=self.clear_console,
        )
        clear_button.pack()
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
            self.log("Initiating connection to server...")
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
        if self.is_clean == False:
            msg[MSG_TYPE_KEY] = CLEAN_MSG_TYPE
            # gather options from checkboxes
            options_list = []
            for i in self.clean_listbox.curselection():
                options_list.append(self.clean_options_labels[i])
            if len(options_list) == 0:
                self.log("CLANG! need to select at least one option for cleaning")
                return
            msg[DATA_KEY] = options_list
        else:
            msg[MSG_TYPE_KEY] = UNCLEAN_MSG_TYPE

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
            MSG_TYPE_KEY: VALIDATE_MSG_TYPE,
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
        self.console.yview_moveto(1.0)

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
            if state == "normal":
                if button != self.clean_button and self.is_clean == False:
                    continue
                    
            button.config(state=state)

    def send_request(self, msg):
        if self.serversocket == None:
            self.init_socket()
        try:
            # disable request buttons
            self.update_request_button_state("disabled")
            # enable cancel request button
            self.cancel_button.config(state="normal")
            self.log("Sending request <{}>...".format(msg[MSG_TYPE_KEY]))
            self.serversocket.send(pickle.dumps(json.dumps(msg)))
            threading.Thread(target=self.wait_for_resp,
                             args=(msg[MSG_TYPE_KEY],)).start()
        except Exception as e:
            traceback.print_exc()
            self.log("CLANG! error while sending request.")
            if self.serversocket != None:
                self.serversocket.close()
            self.serversocket = None
            # enable request buttons
            self.update_request_button_state("normal")
            # disable cancel request button
            self.cancel_button.config(state="disabled")

    def wait_for_resp(self, message_type):
        try:
            self.log("Awaiting response <{}>...".format(message_type))
            resp = self.serversocket.recv(BUFFER_SIZE)
            resp = json.loads(pickle.loads(resp))
            print(resp)
           
            # log results to output
            self.log("Server reponse status: {}".format(resp[STATUS_KEY]))
            if resp[STATUS_KEY] == OK_STR and DATA_KEY in resp:
                self.log("Result: {}".format(resp[DATA_KEY]))
            
            if resp[STATUS_KEY] == OK_STR:
                # toggle clean/unclean button text
                if resp[MSG_TYPE_KEY] == CLEAN_MSG_TYPE:
                    self.clean_str.set("Unclean")
                    self.is_clean = True
                elif resp[MSG_TYPE_KEY] == UNCLEAN_MSG_TYPE:
                    self.clean_str.set("Clean")
                    self.is_clean = False

            # disable cancel request button
            self.cancel_button.config(state="disabled")
            # enable request buttons
            self.update_request_button_state("normal")
        except Exception as e:
            pass

    # unused func

    def cancel_request(self):
        pass
        # if self.serversocket == None:
        #     return
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
    root.geometry("600x700")

    app = Window("ECE656 Project", root)
    root.mainloop()


if __name__ == "__main__":
    main()
