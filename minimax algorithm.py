import pygame
from copy import deepcopy
from checkers.constants import blue, red

'''
board_state = current state of the game
depth = how far will the tree extend. Decreases by 1 recursively
max_player = boolean, True means maximising player, False means minimising player
game = the game object
'''
def minimax(board_state, depth, max_player, game):
    if depth == 0 or board_state.winner() != None:
        return board_state.evaluate(), board_state

    if max_player:
        maxEval = float('-inf')
        best_move = 0
        for move in get_all_moves(board_state, red, game):  # maximising player
            # gets evaluation of each node it is considering
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = 0
        for move in get_all_moves(board_state, blue, game):  # minimising player
            # gets evaluation of each node we are considering
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move


def minimaxAB(board_state, depth, alpha, beta, max_player, game):
    #alpha = 0
    #beta = 0
    # print(type(alpha))
    # print(type(beta))
    if depth == 0:  # or board_state.winner() != None
        return board_state.evaluate(), board_state  # evaluate() is the heuristics
    best_move = None
    if max_player:
        max_eval = float('-inf')
        for move in get_all_moves(board_state, red, game):
            evaluation = minimaxAB(move, depth-1, alpha, beta, False, game)
            # evaluation = minimax_AB(move, depth-1, False, game)[0]
            print(evaluation)
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            # if maxEval == evaluation:
            #best_move = move
            # if maxEval > alpha:
            #alpha = move
            if alpha >= beta:
                break
        #best_move = max_eval
        return max_eval, alpha

    else:
        min_eval = float('inf')
        for move in get_all_moves(board_state, blue, game):
            ev = minimaxAB(move, depth-1, alpha, beta, True, game)
            evaluation = ev[0]
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            # if minEval == evaluation:
            #best_move = move
            # if minEval > beta:
            #beta = move
            if alpha >= beta:
                break
        #best_move = min_eval
        return min_eval, beta


def simulate_move(piece, move, board_state, game, captured):
    board_state.move_piece(piece, move[0], move[1])
    if captured:
        board_state.remove(captured)

    return board_state


# gets all the possible moves you can make 
# at the current state of the board
def get_all_moves(board_state, colour, game):
    # stores the new board
    moves = []

    for piece in board_state.get_all_pieces(colour):
        valid_moves = board_state.get_valid_moves(piece)
        for move, captured in valid_moves.items():
            temp_board = deepcopy(board_state)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(
                temp_piece, move, temp_board, game, captured)
            moves.append(new_board)

    return moves
