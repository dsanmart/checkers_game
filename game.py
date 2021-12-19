import pygame
from constants import red, white, blue, square_size
from board import Board


class Game:
	def __init__(self, win):
		self._init()
		self.win = win

	def update(self):   # Time Complexity: O(m*n). This function checks through each row and column (m and n) and lists out the possible move for each piece on each square.
		self.board.draw(self.win)
		self.draw_valid_moves(self.valid_moves)
		pygame.display.update()

	def _init(self):    # This function just states the base state of the board
		self.selected = None
		self.board = Board()
		self.turn = red
		self.valid_moves = {}

	def winner(self): # Time Complexity: O(1)
		return self.board.winner()

	def reset(self): # Time Complexity: O(1). This function just resets the whole board back to the base state.
		self._init()

	def select(self, row, col): # Time complexity: O(m*n). This function goes through the rows and columns to determine the available moves of the piece that we selected
		if self.selected:
			result = self._move(row, col)
			if not result:
				self.selected = None
				self.select(row, col)

		piece = self.board.get_piece(row, col)
		if piece != 0 and piece.color == self.turn:
			self.selected = piece
			self.valid_moves = self.board.get_valid_moves(piece)
			return True

		return False

	def _move(self, row, col): # Time complexity: O(m*n). This function goes through the rows and columns to figure out the possible moves for a certain piece
		piece = self.board.get_piece(row, col)
		if self.selected and piece == 0 and (row, col) in self.valid_moves:
			self.board.move(self.selected, row, col)
			skipped = self.valid_moves[(row, col)]
			if skipped:
				self.board.remove(skipped)
			self.change_turn()
		else:
			return False

		return True

	def draw_valid_moves(self, moves): # Time Complexity: O(n). This function uses _move() and visualizes the possible squares on the board that a piece can move to.
		for move in moves:
			row, col = move
			pygame.draw.circle(self.win, blue,
			                   (col * square_size + square_size // 2, row * square_size + square_size // 2), 15)

	def change_turn(self):  # Time Complexity: O(1). This function simply just changes the turn of who's playing
		self.valid_moves = {}
		if self.turn == red:
			self.turn = white
		else:
			self.turn = red

	def get_board(self):  # Time Complexity: O(1). Function to return the board to the ai algorithm
		return self.board

	def ai_move(self, board):  # Time Complexity: O(1). Function to draw the moves that the AI has made and pass the turn to the player
		self.board = board
		self.change_turn()
