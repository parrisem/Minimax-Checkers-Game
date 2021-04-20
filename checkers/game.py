import pygame
from .constants import blue, red, white, green, square_size
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    ''' 
    Updates the display of the game after a state change.
    '''

    def update(self):
        self.board.create_board(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.chosen_piece = None
        self.board = Board()
        self.turn = blue
        self.valid_moves = {}

    '''
    Returns the winner that the winner function
     in the board class calculates.
    '''

    def winner(self):
        return self.board.winner()

    '''
    Resets the state of the board.
    '''

    def reset(self):
        self._init()

    '''
    Selects a piece given and moves it to the 
    given row and column.
    '''

    def choose_piece(self, row, col):
        if self.chosen_piece:
            # moves the chosen piece to the given square
            result = self._move_piece(row, col)
            if not result:
                # allows you to choose another piece if the previous one wasn't moved
                self.chosen_piece = None
                self.choose_piece(row, col)
        else:
            piece = self.board.get_piece(row, col)  # get the piece
            if piece != 0 and piece.colour == self.turn:
                self.chosen_piece = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        return False

    '''
    Moves the chosen checker to a valid place on the board. 
    If the chosen piece jumps over a checker of the opponent
    that checker is removed from the board.
    '''

    def _move_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.chosen_piece and piece == 0 and (row, col) in self.valid_moves:
            # moves the chosen piece to a valid selected 
            # position on the board
            self.board.move_piece(self.chosen_piece, row, col)
            captured = self.valid_moves[(row, col)]
            if captured:
                self.board.remove(captured)
            self.change_turn()
        else:
            return False

        return True

    '''
    Highlights all the possible moves for the 
    chosen piece on the borad.
    '''

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.rect(self.win, green, (col * square_size,
                                               row * square_size, square_size, square_size))

    '''
    Changes the turn of the player once the 
    opponent has made a valid move.
    '''

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == blue:
            self.turn = red
        elif self.turn == red:
            self.turn = blue

    '''
    Returns the board.
    '''

    def get_board(self):
        return self.board

    '''
    Generates the AI moves
    '''

    def ai_move(self, board):
        self.board = board
        self.change_turn()