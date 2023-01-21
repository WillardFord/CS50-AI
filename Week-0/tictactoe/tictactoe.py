"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_moves = 0
    for row in board:
        for place in row:
            if place is not EMPTY:
                count_moves +=1
    if count_moves % 2 == 0:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                possible_moves.add((i,j))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if board_copy[action[0]][action[1]] is not None:
        raise ValueError
    board_copy[action[0]][action[1]] = player(board_copy)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # 3 horizontal wins
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            return board[row][0]
    # 3 vertical wins
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            return board[0][col]
    # 2 diagonal wins
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY and winner(board) == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # will is work here?
    if winner(board) == O:
        return -1
    if winner(board) == X:
        return 1
    return 0



## Runs but doesn't give optimal strategy!!

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    moves = actions(board)
    # Player board is X
    if player(board) is X:
        val = -2
        for move in moves:
            min_val = minValue(result(board, move)) 
            if min_val > val:
                val = min_val
                output = move


    # Player board is O
    else:
        val = 2
        for move in moves:
            max_val = maxValue(result(board, move))
            if  max_val < val:
                val = max_val
                output = move
    return output


def maxValue(board):
    if terminal(board):
        return utility(board)
    val = -2
    for action in actions(board):
        val = max(val, minValue(result(board,action)))
    return val

def minValue(board):
    if terminal(board):
        return utility(board)
    val = 2
    for action in actions(board):
        val = min(val, maxValue(result(board,action)))
    return val
