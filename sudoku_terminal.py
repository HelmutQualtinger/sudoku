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

def move(s):
    """
    Gets the move from the user.

    Returns:
        tuple: The move (row, col, candidate).
    """

    while True:
        command = input(
            """Next move:   
<row>=[1-9] <column>=[A-J] <number>=[0-9] or  
<row>=[1-9] <column>=[A-J] F(reeze() or 
<row>=[1-9] <column>=[A-J] U(freeze(9) or
Save <filename>' or Load <filename>' or 'q' to quit)""")
        command = command.lower()
        words = command.split()
        if words[0].startswith('q'): # user wants to quit
            return False
        if words[0][0] == 's':        # user wants to save the game
            if len(words) != 2:
                print("Invalid input", command)
                continue
            filename = words[1]
            s.save_json(filename)
            continue
        if words[0][0]== 'l':       # user wants to load a game
            if len(words) != 2:
                print("Invalid input",command)
                continue
            filename = words[1]
            s.load_json(filename)
            continue
        row = int(words[0][0])-1         
        col = ord(words[1][0].upper()) - ord('A')
        if (not 0 <= col < 9) or (not 0 <= row < 9):
            print("Invalid input",command)
            continue
        if words[2][0] == 'f': # user wants to freeze or unfreeze a field  
            s.freeze(row , col)
            return True
        if words[2][0] == 'u':                          # user wants to unfreeze a field
            s.unfreeze(row , col)
            return True
        number = int(words[2][0])
        if not 0 <= number <= 9:
            print("Invalid input",command)
            continue        
        else:
            s.set_field(row , col, number) # user wants to set a field
            return True9
        if len(words) != 3:
            print("Invalid input")
            continue
    return True

def game_on_terminal():
    """
    The main function to play the Sudoku game.

    Returns:
        None
    """
    sudoku = Sudoku(startboard)

    sudoku.load_json('sudoku.json')  # load Sudoku from file
    goon=True
    while goon:
        print("Fields left: ", sudoku.count_empty_fields())
        print(sudoku)
        goon= move(sudoku)
        
    sudoku.save_json('sudoku.json')  # save Sudoku to file
if __name__ == "__main__":
    # play in pedestrian mode for debugging
    game_on_terminal()
