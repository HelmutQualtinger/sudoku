import numpy as np
import json

class Sudoku:
    def __init__(self, start_board) -> None:
        self.board2d = np.array(start_board, dtype=int)
        self.frozen2d =np.where(self.board2d > 0, True, False)
        
    def save_json(self, filename):
        data = {
                'board': self.board2d.tolist(),
                'frozen': self.frozen2d.tolist()
            }
        try:
            with open(filename, 'w') as file:
                json.dump(data, file)
        except:
            pass
    def load_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.board2d = np.array(data['board'])
            self.frozen2d = np.array(data['frozen'])
        except:
            pass            
        
    def is_valid(self, candidate,row, col):
        if self.frozen2d[row, col]:
            return False
        if candidate == 0:
            return True
        super_row = row // 3
        super_col = col // 3
        return (self.is_valid_row(candidate, row) and
                self.is_valid_col(candidate, col) and
                self.is_valid_super_row_col(candidate, super_row, super_col))
        
    def is_valid_row(self, candidate, row):
        return not np.any(self.board2d[row, :] == candidate)
    
    def is_valid_col(self, candidate, col):
        return not np.any(self.board2d[:, col] == candidate)
    
    def is_valid_super_row_col(self, candidate, super_row, super_col):
        return not np.any(self.board2d[super_row*3:(super_row+1)*3, 3*super_col:3*(super_col+1)] == candidate)

    def __str__(self) -> str:
    
        s = ' ' * 6
        for col in [chr(ord('A') + c_index) for c_index in range(9)]:
            s += f"{col:3}"
            if col in ['C', 'F']:
                s += ' '
        s+= '\n'
        s+= '=' * 44 + '\n'

        for row in range(9):
            s+= f"{row+1:1}   |"
            for col in range(9):
                if self.frozen2d[row, col]:
                    s+="*"
                else:
                    s+=" "
                s += str(self.board2d[row, col]) + ' '
                if col % 3 == 2:
                    s += '|'
            if row % 3 == 2:
                s += '\n+'+ '-' * 40 + '\n'
            else:
                s+= '\n+'+ ' ' * 40 + '\n'
        return s
    
                        
                        

startboard = [
    [1, 2, 3,   4, 5, 6 ,  7, 8, 9],
    [4, 5, 6,   7, 8, 9,   1, 2, 3],
    [7, 8, 9,   1, 2, 3,   4, 5, 6],

    [2, 3, 1,   6, 4, 5,   9, 7, 8],
    [5, 6, 4,   9, 7, 8,   3, 1, 2],
    [8, 9, 7,   3, 1, 2,   6, 4, 5],
    
    [3, 1, 2,   5, 6, 4,   0, 9, 7],
    [6, 4, 5,   8, 9, 7,   2, 3, 1],
    [9, 7, 8,   2, 3, 1,   5, 6, 0],
]

sudoku = Sudoku(startboard)
        
sudoku.load_json('sudoku.json')
while (True):
    print(sudoku)
    row = int(input("Enter row: "))-1
    col = input("Enter col: ")
    col = ord(col) - ord('A')
    candidate = int(input("Enter candidate: "))
    if sudoku.is_valid(candidate, row, col):
        sudoku.board2d[row, col] = candidate
        sudoku.save_json('sudoku.json')
        print(sudoku)
    else:
        print("Invalid move")