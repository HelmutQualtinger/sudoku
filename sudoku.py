# pylint: disable=invalid-name
"""_Allows the user to play Sudoku included in the file sudoku.json.
 Game status is saved to the file sudoku.json, persistently
"""

import json         # for JSON persistent game storage format
import numpy as np  # for 2D array for avoiding slow python loops, use numpz vectorized operations instead

EMPTY_BOARD = [[0]*9]*9  # empty board  load from JSON later
class Sudoku:
    """
    A class representing a Sudoku board.

    Attributes:
        board2d (numpy.ndarray): A 2D array representing the Sudoku board.
        frozen2d (numpy.ndarray): A 2D array indicating which cells are frozen (initial values).

    Methods:
        __init__(self, start_board): Initializes a Sudoku object.
        save_json(self, filename): Save the Sudoku board as a JSON file.
        load_json(self, filename): Loads a Sudoku board from a JSON file.
        is_valid(self, candidate, row, col): Check if a candidate number is valid for a given position in the Sudoku grid.
        is_valid_row(self, candidate, row): Check if a candidate number is valid for a given row.
        is_valid_col(self, candidate, col): Check if a candidate number is valid for a given column.
        is_valid_super_row_col(self, candidate, super_row, super_col): 
            Check if a candidate number is valid for a given super row and super column.
        __str__(self): Returns a string representation of the Sudoku board.
    """

    def __init__(self, start_board=EMPTY_BOARD) -> None:
        """
        Initializes a Sudoku object.

        Parameters:
        start_board (list of list): A 2D list representing the initial Sudoku board. 9x9, 
        with values 0-9. 0 represents an empty cell. Values 1-9 are the initial values of the board.

        Returns:
        None
        """
        self.board2d = np.array(start_board, dtype=int)
        self.frozen2d = np.where(self.board2d > 0, True, False)

    def save_json(self, filename:str):
        """
        Save the Sudoku board as a JSON file. Only cells explicitely declared as frozen are frozen. 
        All other cells are and remain mutable.

        Args:
            filename (str): The name of the file to save the JSON data to.

        Returns:
            None
        """
        data = {
            'board': self.board2d.tolist(),
            'frozen': self.frozen2d.tolist()
        }
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file)
        except:
            print("failed to save to {filename}")

    def load_json(self, filename:str):
        """
        Loads a Sudoku board from a JSON file.
        Only cells explicitely declared as frozen are frozen. All other cells are mutable.
        Allows to save a game in progress.

        Args:
            filename (str): The path to the JSON file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            JSONDecodeError: If the JSON file is not valid.
            
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.board2d = np.array(data['board'])
            self.frozen2d = np.array(data['frozen'])
        except FileNotFoundError:
            print(f"Failed to load from {filename}: File not found.")
        except json.JSONDecodeError:
            print(f"Failed to load from {filename}: Invalid JSON format.")

    def set_field(self, row:int, col:int, candidate:int) -> None:
        """
        Sets the value of a given cell in the Sudoku board. Does not freeze the cell.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        value (int): The value to be set.

        Returns:
        None
        """
        if self.is_valid(candidate, row, col):
            self.board2d[row, col] = candidate
        else:
            print("Invalid move")

    def is_valid(self, candidate:int, row:int, col:int) -> bool:
        """
        Check if a candidate number is valid for a given position in the Sudoku grid.

        Parameters:
        candidate (int): The number to be checked.
        row (int): The row index of the position.
        col (int): The column index of the position.

        Returns:
        bool: True if the candidate number is valid, False otherwise.
        """
        if self.frozen2d[row, col]:  # cannot change frozen cells
            return False
        if candidate == 0:           # can always clear a cell unless it was frozen
            return True
        super_row = row // 3
        super_col = col // 3
        return (not np.any(self.board2d[row, :] == candidate) and
                not np.any(self.board2d[:, col] == candidate) and
                not np.any(self.board2d[super_row*3:(super_row+1)*3,
                                        3*super_col:3*(super_col+1)] == candidate))
        
    def count_empty_fields(self):
        """
        Counts the number of empty fields in the Sudoku board.

        Returns:
            int: The count of empty fields.
        """
        return 81 - np.count_nonzero(self.board2d)

    def __str__(self) -> str:
        """
        Returns a string representation of the Sudoku board.

        Returns:
            str: The string representation of the Sudoku board. Used for printing the board.
        """
        
        # Header lines with column letters
        s = ' ' * 6
        for col in [chr(ord('A') + c_index) for c_index in range(9)]:
            s += f"{col:3}"
            if col in ['C', 'F']: # slightly seperate the 3x3 blocks
                s += ' '
                
        s += '\n'
        s += '=' * 44 + '\n'    # Ruler

        for row in range(9):        # Rows with row numbers for allowing specifying moves
            s += f"{row+1:1}   |"
            for col in range(9):
                if self.frozen2d[row, col]:   # indicate frozen cells with asterisk
                    s += "*"
                else:
                    s += " "
                s += str(self.board2d[row, col]) + ' '
                if col % 3 == 2:     # slightly separate the 3x3 blocks vertically
                    s += '|'
            if row % 3 == 2:         # slightly separate the 3x3 blocks horizontally
                s += '\n+' + '-' * 40 + '\n'
            else:
                s += '\n+' + ' ' * 40 + '\n'
        return s


startboard = [[0]*9]*9  # empty board  load from JSON later


def validate_input(row, col, candidate):
    """
    Validates the input for row, column, and candidate in a Sudoku game.

    Args:
        row (int): The row number.
        col (str): The column letter.
        candidate (int): The candidate number.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    # Validate row
    if not isinstance(row, int) or row < 1 or row > 9:
        return False

    # Validate column
    if not isinstance(col, str) or len(col) != 1 or not col.isalpha() or not col.isupper():
        return False

    # Validate candidate
    if not isinstance(candidate, int) or candidate < 0 or candidate > 9:
        return False

    return True


def game():
    """
    The main function to play the Sudoku game.

    Returns:
        None
    """
    sudoku = Sudoku(startboard)

    sudoku.load_json('sudoku.json')  # load Sudoku from file

    while True:
        print("Fields left: ", sudoku.count_empty_fields())
        print(sudoku)
        row = input("Enter row: ")
        row = int(row)
        col = input("Enter col: ")
        candidate = int(input("Enter candidate: "))
        if not validate_input(row, col, candidate):
            print("Invalid input")
            continue
        col = ord(col.upper()) - ord('A')
        row=int(row)-1
        candidate=int(candidate)
        if sudoku.is_valid(candidate, row, col):
            sudoku.set_field(row, col, candidate)
            sudoku.save_json('sudoku.json')
        else:
            print("Invalid move")
            

if __name__ == "__main__":
    # play in pedestrian mode for debugging
    game()


