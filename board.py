import pygame
from constants import *
from piece import Piece

class Board:
    def __init__(self):
        self.board = [] # use of a multidimensional array of 2 dimensions, where the time complexity of traversing it is an average of O(N*M*...) where N, M, ... is the size of each dimension
        self.red_remaining = self.white_remaining = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win): #drawing the squares for the checkers board. Avg. runtime of O(n). Worst case: O(n^2).
        #fill window with black
        win.fill(black)
        # defining checker board pattern, that is the reason why we use 'row % 2'
        for row in range(rows):
            for col in range(row % 2, cols, 2):
                pygame.draw.rect(win, grey, (row * square_size, col * square_size, square_size, square_size))

    def evaluate(self): # This is to evaluate the score that a move will have. Avg. runtime of O(1). Worst: O(1).
        return self.white_remaining - self.red_remaining + (self.white_kings * 0.5 - self.red_kings * 0.5) # Add score for kings generation as it is an advantage
    
    def get_all_pieces(self, color): # Function to get all the checkers of a certain color in order to later check its possible moves. Avg. runtime of O(n^2). Worst: O(n^2).
        checkers = []
        for row in self.board: # self.board stores all of the checks in a 2d array splited in rows
            for checker in row:
                if checker != 0 and checker.color == color:
                    checkers.append(checker)
        return checkers

    def move(self, piece, row, col): # Avg. runtime of O(n). Worst: O(n^2).
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] #accessing the different dimensions of the array through indexing notation, and swapping the positions of the pieces to simulate the movement
        piece.move(row, col)

        # check to see if current position is the last row, if so, make piece a king
        if row == rows - 1 or row == 0:
            piece.if_king()
            if piece.color == white:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col): # Avg. runtime of O(1). Worst O(1)
        # get the piece to be moved
        return self.board[row][col]

    def create_board(self): # Avg. runtime of O(n). Worst: O(n^2).
        for row in range(rows):
            self.board.append([]) # interior lists for each row of the board
            for col in range(cols):
                if col % 2 == ((row + 1) % 2): # if current column % 2 == ((row + 1) % 2), then we can draw the piece, since the pieces are spaced out
                    if row < 3:
                        self.board[row].append(Piece(row, col, white))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, red))
                    else:
                        self.board[row].append(0) # when we don't add a piece we append 0 to the previously defined multidimensional array
                else:
                    self.board[row].append(0)
        
    def draw(self, win): # Avg. runtime of O(n). Worst: O(n^2).
        # drawing the board and pieces
        self.draw_squares(win)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):  # Time Complexity: O(n). Worst: O(n^2). The remove() function goes through each row and column (m*n) and checks its conditions based on that location layout
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == red:
                    self.red_remaining -= 1
                else:
                    self.white_remaining -= 1
    
    def winner(self): # Avg. runtime of O(1). Worst: O(n). The winner() function simply determines the winner of the game by checking which color player lost all their pieces first. The function simply just checks the remaining pieces of each color.
        if self.red_remaining <= 0:
            winner_player = "white"
            return winner_player
        elif self.white_remaining <= 0:
            winner_player = "red"
            return winner_player
        
        return None 
    
    def get_valid_moves(self, piece): # Time Complexity: O(n). Worst: O(n). This function updates the possible moves of all the pieces on the board using an if loop
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        if piece.color == red or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == white or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, rows), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, rows), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]): # Time Complexity : O(n).Worst: O(n^2). This function has nested loops inside a loop, each with a time complexity of O(n) as the moves decrement on each run of the loop
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, rows)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]): # Time Complexity : O(n).Worst: O(n^2). This function has nested loops inside a loop, each with a time complexity of O(n) as the moves decrement on each run of the loop
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= cols:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, rows)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
