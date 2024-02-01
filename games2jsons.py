import numpy
import sudoku as s
#  Translate the terse format sudoko file into a set of json files 
with open("games/games.txt") as games_file:
    lines=games_file.readlines()
    
    for game in range(50):
        board=s.Sudoku(s.EMPTY_BOARD)   # create empty board
        lines=lines[1:]                 # remove header
        for row in range(9):            # loop over all rows
            for col in range(9):        # and columns
                board.board2d[row,col]=int(lines[row][col]) # set the number
                
        board.frozen2d=numpy.where(board.board2d>0,True,False)
        board.save_json(f"games/game{game}.json")
        lines=lines[9:]
    
    
