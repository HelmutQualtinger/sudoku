import numpy as np

class Sudoku:
    def __init__(self, start_board) -> None:
        self.board2d = np.array(start_board, dtype=int)
        self.board4d = self.transpose2d_4d()
        self.frozen2d =np.where(self.board2d > 0, True, False)
        self.frozen4d = np.where(self.board4d > 0, True, False)
        
    def transpose2d_4d(self):
        board4d = np.zeros((3, 3, 3, 3), dtype=int)
        for super_row in range(3):
            for super_col in range(3):
                for row in range(3):
                    for col in range(3):
                        old_row = super_row * 3 + row
                        old_col = super_col * 3 + col
                        board4d[super_row, super_col, row,
                                col] = self.board2d[old_row, old_col]
        return board4d
    
    def transpose4d_2d(self):
        board2d=np.zeros((9, 9), dtype=int)
        for super_row in range(3):
            for super_col in range(3):
                for row in range(3):
                    for col in range(3):
                        new_row =  super_row * 3 + row
                        new_col =  super_col * 3 + col
                        board2d[new_row, new_col] = self.board4d[super_row, super_col, row, col]
        return board2d
    
    def is_valid(self, candidate,row, col):
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
        return not np.any(self.board4d[super_row, super_col, :, :] == candidate)

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
        
        
print(sudoku.board2d)

print(sudoku.board4d)

print(sudoku.frozen2d)
print(sudoku.frozen4d)

print (sudoku)


while (True):
    row = int(input("Enter row: "))-1
    col = input("Enter col: ")
    col = ord(col) - ord('A')
    candidate = int(input("Enter candidate: "))
    if sudoku.is_valid(candidate, row, col):
        sudoku.board2d[row, col] = candidate
        sudoku.board4d = sudoku.transpose2d_4d()
        print(sudoku)
    else:
        print("Invalid move")