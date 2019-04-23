from tkinter import *
import tkinter as tk
from tkinter import scrolledtext

CLEAN_STR = "Clean"
UNCLEAN_STR = "Unclean"
BUTTON_WIDTH = 20


class Window(Frame):

    def __init__(self, title, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.title = title
        self.clean_str = StringVar()
        self.clean_str.set(CLEAN_STR)
        self.analyze_int = IntVar()
        self.analyze_int.set(1)
        self.console_index = 0
        self.clean_options_labels = [
            "Missing SchoolIDs",
            "Missing playerIDs from HOF",
            "Missing teamIDs from Salary",
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
        self.query_types_labels = [
            "HoF Nomination",
            "HoF Entry",
            "Player-to-Manager",
        ]
        self.init_window()

    # Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title(self.title)
        # self.status = tk.Label(self.master, textvariable=self.status_str)
        # self.status.pack(fill="both", side="left")

        # cleaning setup
        self.clean_frame = tk.LabelFrame(self.master, text="Data Cleaning")
        self.clean_frame.pack(fill="both", expand="yes")
        # cleaning options
        self.clean_options_frame = tk.LabelFrame(
            self.clean_frame, text="Cleaning Options")
        self.clean_options_frame.pack(side="left", expand="yes")
        self.clean_checkboxes = []
        for label in self.clean_options_labels:
            chk_state = BooleanVar()
            chk_state.set(True)
            chk = Checkbutton(self.clean_options_frame, text=label,
                              var=chk_state, anchor='w')
            chk.pack(side='bottom')
            self.clean_checkboxes.append(chk)
        # clean button
        clean_button = tk.Button(
            self.clean_frame,
            textvariable=self.clean_str,
            width=BUTTON_WIDTH,
            command=self.clean_unclean,
        )
        clean_button.pack(side="right")

        # analysis setup
        self.analysis_frame = tk.LabelFrame(self.master, text="Data Analysis")
        self.analysis_frame.pack(fill="both", expand="yes")
        # analysis options frame
        self.analysis_options_frame = tk.LabelFrame(
            self.analysis_frame, text="Analysis Options")
        self.analysis_options_frame.pack(side="left", expand="yes")
        self.query_table_box = tk.Listbox(self.analysis_options_frame,
                                          selectmode="multiple")
        self.query_table_box.pack(side='left', expand='yes')
        for i in range(len(self.query_table_labels)):
            self.query_table_box.insert(i+1, self.query_table_labels[i])
        # analysis type frame
        self.analysis_type_frame = tk.LabelFrame(
            self.analysis_frame, text="Analysis Type")
        self.analysis_type_frame.pack(side='left', expand='yes')
        self.query_radio_buttons = []
        for i in range(len(self.query_types_labels)):
            r = tk.Radiobutton(self.analysis_type_frame,
                               text=self.query_types_labels[i],
                               variable=self.analyze_int,
                               value=i + 1,
                               anchor='w')
            r.pack()
            self.query_radio_buttons.append(r)
        query_button = tk.Button(
            self.analysis_frame,
            text="Analyze",
            width=BUTTON_WIDTH,
            command=self.analyze,
        )
        query_button.pack(side="right")

        clear_button = tk.Button(
            self.master,
            text="Clear",
            width=BUTTON_WIDTH,
            command=self.clear_console,
        )
        clear_button.pack(side="bottom")
        # results
        self.result_frame = tk.LabelFrame(self.master, text="Result")
        self.result_frame.pack(fill="both", expand="yes")
        self.console = scrolledtext.ScrolledText(self.result_frame)
        self.console.pack(fill="both", expand="yes")

    def clean_unclean(self):
        if self.clean_str.get() == CLEAN_STR:
            self.print("Uncleaning...")
            # do unclean logic
            self.clean_str.set(UNCLEAN_STR)
            self.print("Uncleaned!")
        else:
            self.print("Cleaning...")
            # do cleaning logic
            self.clean_str.set(CLEAN_STR)
            self.print("Cleaned!")

    def analyze(self):
        self.print("Analysing...")
        self.print("Analyszed!")

    def print(self, msg):
        self.console.insert(tk.INSERT, "{}\n".format(msg))

    def clear_console(self):
        self.console.delete(1.0, tk.END)


root = Tk()

# size of the window
root.geometry("700x600")

app = Window("ECE656 Project", root)
root.mainloop()
