from copy import deepcopy
from constants import red, white
import pygame

# The minimax algorithm creates a recursive binary tree that has a time complexity of O(b^d), 
# where b is the number of legal moves at each point and d is the maximum depth of the tree.
# However, as we are using alpha-beta pruning we have time complexity for the best case which is O(b^(d/2))
# Hence, the worst case scenario is O(b^d) and best case is O(b^(d/2))

def minimax(board, tree_depth, alpha, beta, cpu_turn, gamefunc):
    if tree_depth == 0 or board.winner() != None:
        return board.evaluate(), board

    if cpu_turn:
        max_score = float('-inf')
        best_move = None
        for move in get_all_moves(board, white, gamefunc):
            score = minimax(move, tree_depth - 1, alpha, beta, False, gamefunc)[0] # To reduce memory usage we only get the score [0] when calling this recursive function (not the best_move)
            max_score = max(max_score, score)
            if max_score == score:
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in get_all_moves(board, red, gamefunc):
            score = minimax(move, tree_depth - 1, alpha, beta, True, gamefunc)[0] # To reduce memory usage we only get the score [0] when calling this recursive function (not the best_move)
            min_score = max(min_score, score)
            if min_score == score:
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score, best_move


def get_all_moves(board, color, gamefunc): # Time complexity: O(n*m). Worst case: O(n*m) This function goes through all the left pieces of a color (n) and then checks the possible moves (m)
    moves = []

    for checker in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(checker)

        for move, skip in valid_moves.items():
            board_copy = deepcopy(board)
            checker_copy = board_copy.get_piece(checker.row, checker.col)
            new_board = simulate_move(checker_copy, move, board_copy, gamefunc, skip)
            moves.append(new_board)

    return moves

def simulate_move(checker, move, board, gamefunc, skip): # Time complexity: O(1). Worst case: O(1). This function simulates a move by moving and removing it
    board.move(checker, move[0], move[1])
    if skip:
        board.remove(skip)
    
    return board
