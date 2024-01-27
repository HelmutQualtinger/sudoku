import tkinter as tk
import sudoku as s
import random

class SudokuTk(tk.Tk):
    """
    The Sudoku game class.
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
        self.create_widgets()
        
    def set_field(self, event,row, col,press):
        if not press:
            self.Buttons[(row,col)].config(relief=tk.RAISED,bg="#80f080")
            print("relase",row,col)
            return
        self.Buttons[(row,col)].config(relief=tk.SUNKEN,bg="#00ff00")
        print("set_field",row,col)

    def create_widgets(self):
        """
        Creates the widgets for the Sudoku game.

        Returns:
            None
        """
        Button = dict()
        for i in range(9):
            for j in range(9):
                
                button_text = str(self.board.board2d[i,j])
                button = tk.Label(self, width=3, height=2, justify='center', text=button_text,
                                  bg="#80f080", relief=tk.RAISED, fg='#000000', font=("Helvetica", 16), borderwidth=4)
#                                   command=lambda row=i, col=j: self.set_field(row, col))

                button.bind("<ButtonPress-1>", lambda event,row=i,col=j: self.set_field(event,row,col,1))
                button.bind("<ButtonRelease-1>", lambda event,row=i,col=j: self.set_field(event,row,col,0))  # Add this line for button release binding
                button.bind("<Leave>", lambda event, row=i, col=j: self.set_field(event, row, col,0))

                
                button.grid(row=i, column=j)
                Button[(i,j)] = button
                if self.board.frozen2d[i,j]:
                    Button[(i,j)].config(bg="#000000",fg="#ffffff",font=("Arial", 16,"bold"))


        self.Buttons=Button
        self.button = tk.Button(self, text="Solve", command=self.solve)
        self.button.grid(row=9, column=0, columnspan=9)
        
    def solve(event):
        """
        Solves the Sudoku game.

        Returns:
            None
        """
        exit()
    def report_callback_exception(exc, val, tb,more):
        print("report_callback_exception",exc, val, tb)


sudoku= s.Sudoku(s.EMPTY_BOARD)
sudoku.load_json('sudoku.json')
app = SudokuTk(sudoku)
app.mainloop()