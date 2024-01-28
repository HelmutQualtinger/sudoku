import json
import os
from sudoku import Sudoku

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


def game_on_terminal():
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
    game_on_terminal()
