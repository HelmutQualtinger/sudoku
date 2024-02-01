# pylint: disable=unused-argument
import tkinter as tk
from tkinter import Menu, filedialog
import itertools
import sys
import simpleaudio as sa


def play_wav(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()


# Replace 'your_file.wav

import sudoku as s
class SudokuTk(tk.Tk):
    """
    The Sudoku GUI interface game class using Tkinter.
    Inherits from tk.Tk and uses the Sudoku class in  composition
    the bare bones Sudoku game is created stored in self.board

    """

    def __init__(self, board):
        """
        Initializes the Sudoku game.

        Args:
            board (class sudoku): The Sudoku board.
            master (tk.Tk): The Tkinter root window.

        Returns:
            None
        """
        super().__init__()   # do whatever Tkinter does
        self.board = board   # link to the Sudoku board
        self.active_number = 0  # no active number yet
        self.create_widgets()  # create the widgets
        self.update_widgets()  # update the widgets for the first time
        # to make sure session saved whatever way we exit
        self.bind("<Destroy>", lambda e: self.quit)
        # to make sure session saved whatever way we exit
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def set_active_number(self, number):
        # set the active number, set in the callbacks of the Buttons and the Labels
        # used to color the Labels and Buttons
        self.active_number = number
        self.update_widgets()  # update the widgets

    # handles mouse click events called from command lambdas
    def set_field(self, event, row, col, bt, action):
        print(event, row, col, bt, action)
        # mouse enters a field, make the number it contains active:
        if action == "Enter":
            self.active_number = self.board.board2d[row, col]
            self.update_widgets()
            return
        # adjust the relief and color of the button
        if bt==1:
            if action == "Release" and not self.board.frozen2d[row, col]:
                self.Buttons[(row, col)].config(relief=tk.RAISED)
                print("release button 1", row, col)
                return
            if action == "Press" and not self.board.frozen2d[row, col]:
                self.Buttons[(row, col)].config(relief=tk.RAISED, bg="#00ff00")
                popup_menu = Menu(self, tearoff=0)
                #  only candidates are allowed, only they are added to the popup menu
                candidate_list = self.board.get_candidates(row, col)
                if not self.board.board2d[row, col] == 0:
                    # if the field is not empty, add 0 option to clear it
                    candidate_list |= {0}
                # add the candidates to the popup menu and if applicable the clear option
                for i in candidate_list:
                    if i == 0:
                        label = "Clear"
                    else
                        label = str(i)
                    # schedule the Sudoku method for manipulation of the board
                    popup_menu.add_command(label=label,
                                        command=lambda row=row, col=col, i=i: self.board.set_field(row, col, i))
#                    if self.board.count_empty_fields() == 0:                       

                # show the popup menu on screen
                popup_menu.post(event.x_root, event.y_root)
                if self.board.count_empty_fields() < 81:
                    play_wav('youwon.wav')
        #     print("posted", row, col)
        #     print("set_field", row, col)
        if bt == 2:  # right mouse button used for freezing and unfreezing the initial board cells, 
                     # seem to get onl release events
            popup_menu = Menu(self, tearoff=0)
            if self.board.frozen2d[row, col]:
                popup_menu.add_command(label="Unfreeze",
                                        command=lambda row=row, col=col: self.board.unfreeze(row, col))
            else:
                popup_menu.add_command(label="Freeze",
                                        command=lambda row=row, col=col: self.board.freeze(row, col))
            popup_menu.post(event.x_root, event.y_root)
        # make the field in the mouse event the number active
        self.active_number = self.board.board2d[row, col]
        self.update_widgets()   # update the widget colors

    def create_widgets(self):
        """
        Creates the widgets for the Sudoku game.

        Returns:
            None
        """
        # create TOP menu with load save buttons and candidate list
        self.top_frame = tk.Frame(self, borderwidth=2)
        self.top_frame.grid(row=0, column=0, columnspan=9, padx=5, pady=5)

        self.load_button = tk.Button(self.top_frame, text="Load",
                                     command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=1, pady=1)
        self.save_button = tk.Button(self.top_frame, text="Save",
                                     command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=1, pady=1)
        self.numbers = []
 # create hover row with numbers to show where they are on the board
        for i in range(9):
            ll = tk.Label(self.top_frame, text=str(i+1), relief=tk.FLAT,
                          font=("Helvetica", 14, "italic"))
            ll.pack(side=tk.LEFT, padx=1, pady=1)
            # picked up by update_widgets in coloring
            ll.bind("<Enter>", lambda event, i=i+1: self.set_active_number(i))
            ll.bind("<Leave>", lambda event, i=i+1: self.set_active_number(0))
            self.numbers.append(ll)
# how many fields still to go, 0 means solved
        self.free_fields = tk.Label(self.top_frame, text="Free fields: 0",

                                    font=("Helvetica", 16, "bold"))
        self.free_fields.pack(side=tk.LEFT, padx=1, pady=1)
# super frame for the 3x3 grid frames
        self.button_frame = tk.Frame(self, borderwidth=2, relief="solid")
        self.button_frame.grid(row=1, column=0, columnspan=9, padx=5, pady=5)
        Button = {}
        for super_row in range(3):
            for super_col in range(3):
                # create 3x3 grid frames
                frame = tk.Frame(self.button_frame,
                                 borderwidth=2, relief="solid")
                frame.grid(row=super_row, column=super_col, padx=5, pady=5)
                for i in range(3):
                    for j in range(3):
                        # in each frame created 3x3 buttons, really labels because buttons cannot be styled on the Mac
                        row2d = super_row * 3 + i
                        col2d = super_col * 3 + j
                        button_text = str(self.board.board2d[row2d, col2d])
                        button = tk.Label(frame, width=3, height=2, justify='center', text=button_text,
                                          bg="#80f080", relief=tk.RAISED, fg='#000000',
                                          font=("Helvetica", 14),
                                          borderwidth=4)
                        for bt, action in zip(range(1, 3), ["Press", "Release"]):
                            button.bind(f"<Button{action}-{bt}>",
                                        lambda event, row=row2d, col=col2d, bt=bt, action=action: self.set_field(event, row, col, bt, action))
                        button.bind("<Enter>", lambda event, row=row2d, col=col2d: self.set_field(
                            event, row, col, 3, "Enter"))
                        button.grid(row=i, column=j)
                        # remember widget for later reference
                        Button[(row2d, col2d)] = button
        # add the buttons to the object they are really labels because buttons cannot be styled on the Mac
        self.Buttons = Button
# create bottom frame with quit button
        self.q_button = tk.Button(self, text="Quit", command=self.quit)
        self.q_button.grid(row=9, column=0, columnspan=9, sticky="nsew")
        self.q_button.grid_rowconfigure(0, weight=1)
        self.q_button.grid_columnconfigure(0, weight=1)

        self.title("Assisted Sudoku")

    def update_widgets(self):
        # Set the colors of the widgets according to the state of the board and the active number
        self.free_fields.config(text="Free fields: " +
                                str(self.board.count_empty_fields()),relief=tk.RAISED)
        for (row, col) in itertools.product(range(9), range(9)):  # over all rows and columns
            if self.board.frozen2d[row, col]:
                self.Buttons[(row, col)].config(relief=tk.SUNKEN)
            else:
                self.Buttons[(row, col)].config(relief=tk.RAISED)
            digit_str = str(
                self.board.board2d[row, col] if self.board.board2d[row, col] else "")
            # default black on white
            self.Buttons[(row, col)].config(text=digit_str, bg="#ffffff", fg="#000000",
                                            )
            # empty fields are light green to start with
            if self.board.board2d[row, col] == 0:
                self.Buttons[(row, col)].config(
                    text=digit_str)  # set the number
                self.Buttons[(row, col)].config(
                    bg="#80ff80", fg="#80ff80")
            # frozen fields are gray
            if not self.active_number == 0:  # non-candidates are light red
                # candidates are light red
                if (not self.active_number in (self.board.get_candidates(row, col)-{0})
                    and not self.board.frozen2d[row, col]):
                    self.Buttons[(row, col)].config(bg="#ff8080")
                # active number is red
                if self.board.board2d[row, col] == self.active_number:
                    self.Buttons[(row, col)].config(bg="#c00000")
            if not self.board.frozen2d[row, col] and self.board.board2d[row, col] == 0 and len(self.board.get_candidates(row, col)) < 2:
                # fields with only one candidate are yellow,easy prez
                self.Buttons[(row, col)].config(bg="#ffFFc0", fg="#000000")
 

    def quit(self):
        """
        Exits the Sudoku game.


        Returns:
            None
        """
        sudoku.save_json('sudoku.json')  # save the session persistently
        print("Quitting after saving session")
        sys.exit(0)

    def load_file(self):

        filename = filedialog.askopenfilename(
            title="Select Sudoku File:", filetypes=[("JSON Files", "*.json")])
        if filename:
            print("Loading file", filename)
            self.board.load_json(filename)
            self.update_widgets()

    def save_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save as Sudoku file:", filetypes=[("Save as JSON File", "*.json")])
        if filename:
            print("Saving file", filename)
            self.board.save_json(filename)

    def report_callback_exception(self, exc, val, tb, *args):
        # needed to catch exceptions in callbacks not in parent frame class
        print("report_callback_exception", exc, val, tb)


sudoku = s.Sudoku(s.EMPTY_BOARD)  # create the Sudoku board empty
sudoku.load_json('sudoku.json')  # load the last session, if any
app = SudokuTk(sudoku)           # create the GUI
app.mainloop()                   # activate the GUI

sudoku.save_json('sudoku.json')  # save the session persistently
