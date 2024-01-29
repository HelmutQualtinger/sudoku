# pylint: disable=unused-argument
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
import itertools
import sys
import sudoku as s


class SudokuTk(tk.Tk):
    """
    The Sudoku GUI interface game class.
    """

    def __init__(self, board):
        """
        Initializes the Sudoku game.

        Args:
            board (list): The Sudoku board.
            master (tk.Tk): The Tkinter root window.

        Returns:
            None
        """
        super().__init__()
        self.board = board
        self.active_number = 0
        self.create_widgets()
        self.update_widgets()
        
        
    def set_active_number(self, number):
        self.active_number = number
        self.update_widgets()
        
    def set_field(self, event, row, col, press):
        print (event, row, col, press)
        if not press:
            self.Buttons[(row, col)].config(relief=tk.RAISED, bg="#80f080")
            print("release", row, col)
            return
        self.Buttons[(row, col)].config(relief=tk.SUNKEN, bg="#00ff00")
        popup_menu = Menu(self, tearoff=0)
        for i in self.board.get_candidates(row, col)|{42,0}:
            if i == 0:
                label="Clear"
            else:
                label=str(i)
            popup_menu.add_command(label=label
                                   , command=lambda row=row, col=col, i=i: self.board.set_field(row, col, i))
        popup_menu.post(event.x_root, event.y_root)
        print("posted", row, col)
        print("set_field", row, col)
        self.active_number = self.board.board2d[row, col]
        self.update_widgets()
        
    def create_widgets(self):
        """
        Creates the widgets for the Sudoku game.

        Returns:
            None
        """
        # create TOP menu with load save buttons and candidate list
        self.top_frame = tk.Frame(self, borderwidth=2)
        self.top_frame.grid(row=0, column=0, columnspan=9, padx=5, pady=5)
        self.numbers = []
        
        self.load_button = tk.Button(self.top_frame, text="Load",
                                    command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=1, pady=1)
        for i in range(9):
            ll=tk.Label(self.top_frame, text=str(i+1),relief=tk.FLAT,
                        font=("Helvetica", 14, "italic"))
            ll.pack(side=tk.LEFT, padx=1, pady=1)
            ll.bind("<Enter>", lambda event, i=i+1:self.set_active_number(i))
            ll.bind("<Leave>", lambda event, i=i+1:self.set_active_number(0))
            self.numbers.append(ll)
            
            
        self.save_button = tk.Button(self.top_frame, text="Save", 
                                    command= self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=1, pady=1)

        self.button_frame = tk.Frame(self, borderwidth=2, relief="solid")
        self.button_frame.grid(row=1, column=0, columnspan=9, padx=5, pady=5)
        Button = dict()
        for super_row in range(3):
            for super_col in range(3):
                frame = tk.Frame(self.button_frame, borderwidth=2, relief="solid")
                frame.grid(row=super_row, column=super_col, padx=5, pady=5)
                for i in range(3):
                    for j in range(3):
                        row2d = super_row * 3 + i
                        col2d = super_col * 3 + j
                        button_text = str(self.board.board2d[row2d, col2d])
                        button = tk.Label(frame, width=3, height=2, justify='center', text=button_text,
                                        bg="#80f080", relief=tk.RAISED, fg='#000000', 
                                        font=("Helvetica", 14),
                                        borderwidth=4)
        #                                  command=lambda row=r, col=j: self.set_field(row, col))
        # Add this line for simulated button bindings
                        button.bind("<ButtonPress-1>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 1))
                        button.bind("<ButtonRelease-1>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 0))                      
                        button.bind("<ButtonPress-2>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 1))
                        button.bind("<ButtonRelease-2>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 0))
                        button.bind("<ButtonPress-3>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 1))
                        button.bind("<ButtonRelease-3>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 0))
#                        button.bind("<Leave>",
#                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 0))

                        button.grid(row=i, column=j)
                        Button[(row2d, col2d)] = button
                        if self.board.frozen2d[row2d, col2d]:
                            Button[(row2d, col2d)].config(bg="#000000",
                                                fg="#ffffff", font=("Arial", 18, "bold"))

        self.Buttons = Button
        self.qbutton = tk.Button(self, text="Quit", command=self.quit)
        self.qbutton.grid(row=9, column=0, columnspan=9, sticky="nsew")
        self.qbutton.grid_rowconfigure(0, weight=1)
        self.qbutton.grid_columnconfigure(0, weight=1)

        self.title("Assisted Sudoku")
        

    def update_widgets(self):
        for (row,col) in itertools.product(range(9), range(9)):  # over all rows and columns

            digit_str=str(self.board.board2d[row,col] if self.board.board2d[row,col] else "")
            # default sunken black on white
            self.Buttons[(row,col)].config(text=digit_str,                                            
                            bg="#ffffff", 
                            fg="#000000",
                            relief=tk.SUNKEN)
            if self.board.board2d[row,col] == 0:        # empty fields are light green
                self.Buttons[(row,col)].config(text=digit_str)  # set the number 
                self.Buttons[(row,col)].config(bg="#ffffff", 
                                               fg="#80ff80",
                                               relief=tk.RAISED)
            if self.board.frozen2d[row,col]:                 # frozen fields are gray
                self.Buttons[(row,col)].config(text=str(self.board.board2d[row,col]), 
                                               bg="#808080", 
                                               fg="#000000",
                                               relief=tk.SUNKEN)
            elif self.board.board2d[row,col] == 0:        # empty fields are light green
                self.Buttons[(row,col)].config(text="", 
                                               bg="#ffffff", 
                                               fg="#80ff80",
                                               relief=tk.RAISED)
            else:
                self.Buttons[(row,col)].config(text=str(self.board.board2d[row,col]),  # filled fields are white
                                               bg="#ffffff", 
                                               fg="#000000",
                                               relief=tk.SUNKEN)
            if (not self.active_number == 0 and 
                not self.board.board2d[row,col] in self.board.get_candidates(row,col)): # candidates are light red
                self.Buttons[(row,col)].config(bg="#ff8080")
            if self.board.board2d[row,col] == self.active_number: # active number is red
                self.Buttons[(row,col)].config(bg="#c00000")
    
    def quit(self):
        """


        Returns:
            None
        """
        sys.exit(0)
        
    def load_file(self,filename=None, ignore_discard=False, ignore_expires=False):
 
            filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
            if filename:
                print ("Loading file",filename)
                self.board.load_json(filename)
                self.update_widgets()
            
    def save_file(self,filename=None, ignore_discard=False, ignore_expires=False):
        filename = filedialog.asksaveasfilename(filetypes=[("JSON Files", "*.json")])
        if filename:
            print("Saving file",filename)
            self.board.save_json(filename)

    def report_callback_exception(self, exc, val, tb, *args):
        print("report_callback_exception", exc, val, tb)




# root = tk.Tk()
# root.title("Sudoku")


sudoku = s.Sudoku(s.EMPTY_BOARD)
sudoku.load_json('sudoku.json')
app = SudokuTk(sudoku)
app.mainloop()

