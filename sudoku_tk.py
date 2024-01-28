# pylint: disable=unused-argument
import tkinter as tk
import sys
import sudoku as s


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

    def set_field(self, event, row, col, press):
        if not press:
            self.Buttons[(row, col)].config(relief=tk.RAISED, bg="#80f080")
            print("release", row, col)
            return
        self.Buttons[(row, col)].config(relief=tk.SUNKEN, bg="#00ff00")
        print("set_field", row, col)

    def create_widgets(self):
        """
        Creates the widgets for the Sudoku game.

        Returns:
            None
        """
        Button = dict()
        for super_row in range(3):
            for super_col in range(3):
                frame = tk.Frame(self, borderwidth=2, relief="solid")
                frame.grid(row=super_row, column=super_col, padx=5, pady=5)
                for i in range(3):
                    for j in range(3):
                        row2d = super_row * 3 + i
                        col2d = super_col * 3 + j
                        button_text = str(self.board.board2d[row2d, col2d])
                        button = tk.Label(frame, width=3, height=2, justify='center', text=button_text,
                                        bg="#80f080", relief=tk.RAISED, fg='#000000', 
                                        font=("Helvetica", 16),
                                        borderwidth=4)
        #                                  command=lambda row=r, col=j: self.set_field(row, col))
        # Add this line for simulated button bindings
                        button.bind("<ButtonPress-1>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 1))
                        button.bind("<ButtonRelease-1>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 0))
                        button.bind("<Leave>",
                                    lambda event, row=row2d, col=col2d: self.set_field(event, row, col, 0))

                        button.grid(row=i, column=j)
                        Button[(row2d, col2d)] = button
                        if self.board.frozen2d[row2d, col2d]:
                            Button[(row2d, col2d)].config(bg="#000000",
                                                fg="#ffffff", font=("Arial", 16, "bold"))

        self.Buttons = Button
        self.button = tk.Button(self, text="Quit", command=self.quit)
        self.button.grid(row=9, column=0, columnspan=9)

    def quit(self):
        """
        Solves the Sudoku game.

        Returns:
            None
        """
        sys.exit(0)

    def report_callback_exception(self, exc, val, tb, *args):
        print("report_callback_exception", exc, val, tb)


sudoku = s.Sudoku(s.EMPTY_BOARD)
sudoku.load_json('sudoku.json')
app = SudokuTk(sudoku)
app.mainloop()

