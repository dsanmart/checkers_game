from constants import red, white, square_size, grey, CROWN
import pygame

# creating the actual pieces
class Piece:
    # padding and outline for pieces position and border
    pad = 15
    outline = 2

    def __init__(self, row, col, color): # Avg. Runtime of O(1). Worst: O(1).
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_pos()

    def calculate_pos(self): # Avg. runtime of O(1). Worst: O(1).
        # calculating the middle of the square for placing the piece
        self.x = square_size * self.col + square_size // 2
        self.y = square_size * self.row + square_size // 2

    def if_king(self): # Avg. runtime of O(1). Worst: O(1).
        # change king variable if piece becomes a king
        self.king = True
    
    def draw(self, win): # Avg. runtime of O(n). Worst: O(n).
        # drawing the piece
        rad = square_size//2 - self.pad # calculating radius
        pygame.draw.circle(win, grey, (self.x, self.y), rad + self.outline) # drawing outer piece
        pygame.draw.circle(win, self.color, (self.x, self.y), rad) # drawing inner piece
        if self.king: # blit the crown for the king piece
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col): # Avg. runtime of O(1). Worst: O(1).
        self.row = row
        self.col = col
        self.calculate_pos()
