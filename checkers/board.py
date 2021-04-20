import pygame
from .constants import black, white, red, blue, rows, cols, square_size, width, height
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.blue_left = 12
        self.red_kings = self.blue_kings = 0
        self.draw_board()

    '''
    Creates the checker board pattern and displays it on the window.
    '''

    def draw_squares(self, win):
        win.fill(black)
        for row in range(rows):
            for col in range(row % 2, cols, 2):
                pygame.draw.rect(win, white, (row * square_size,
                                              col * square_size, square_size, square_size))

    '''
    Moves a checker piece to a new position on the board. 
    It make a checker piece king if it moves into either 
    the first row or the last row of the board.
    '''

    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move_piece(row, col)

        if row == rows - 1 or row == 0:
            piece.is_king()
            if piece.colour == red:
                self.red_kings += 1
            else:
                self.blue_kings += 1

    '''
    Returns the score of the board by subtracting the total number of red pieces from 
    the total number of blue piece on the board.
    '''

    def evaluate(self):
        return self.red_left - self.blue_left + (self.red_kings * 2 - self.blue_kings * 2)

    '''
    Returns a list of all the checker pieces on the board.
    '''

    def get_all_pieces(self, colour):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.colour == colour:
                    pieces.append(piece)
        return pieces

    '''
    Returns the piece on the the board given a set of coordiantes.
    '''

    def get_piece(self, row, col):
        return self.board[row][col]

    '''
    Creates a board with all the checker pieces on it in the right positions.
    '''

    def draw_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, red))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, blue))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    '''
    Displays the initilaised board from the draw_board function onto the window.
    '''

    def create_board(self, win):
        self.draw_squares(win)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(win)

    '''
    Removes a piece from the board and subtracts it from 
    the total number of that colour on the board.
    '''

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.colour == blue:
                    self.blue_left -= 1
                else:
                    self.red_left -= 1

    '''
    Calculates the winner of the game by checking the amount of each colour on the board.
    '''

    def winner(self):
        if self.blue_left <= 0:
            #print('RED WON!')
            return red
        elif self.red_left <= 0:
            #print('BLUE WON!')
            return blue

        return None

    '''
    Uses the _search_left and _search_right functions to determine 
    the valid moves for a piece on the board depending on the 
    colour of that piece. Returns all the valid moves for a chosen 
    piece on the board.
    '''

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        # Decides whether you can move up or down
        # based on the colour of the piece in that position
        if piece.colour == blue or piece.king:
            # down left
            moves.update(self._search_left(
                row - 1, max(row - 3, -1), -1, piece.colour, left))
            # down right
            moves.update(self._search_right(
                row - 1, max(row - 3, -1), -1, piece.colour, right))

        if piece.colour == red or piece.king:
            # up left
            moves.update(self._search_left(
                row + 1, min(row + 3, rows), 1, piece.colour, left))
            # up right
            moves.update(self._search_right(
                row + 1, min(row + 3, rows), 1, piece.colour, right))

        return moves

    '''
    Searches for all valid moves to the left of the chosen piece including possible capture moves.
    It determines what row it will start the search, the row it will stop the search, the direction 
    of the search (i.e. going up to the left or down to the left depending on the colour of the piece), 
    how much it will move along by and keeps a list of all possible capture moves.
    Returns the the moves
    '''

    def _search_left(self, start, stop, step, colour, left, captured=[]):
        moves = {}
        last = []
        #r = row
        for r in range(start, stop, step):
            #left = column
            if left < 0:
                break
            curr_piece = self.board[r][left]
            if curr_piece == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(r, left)] = last + captured
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)

                    else:
                        # uses recursion to check if a piece
                        # can make a double or triple capture move
                        row = min(r + 3, rows)
                    moves.update(self._search_left(
                        r + step, row, step, colour, left - 1, captured=last))
                    moves.update(self._search_right(
                        r + step, row, step, colour, left + 1, captured=last))
                break

            elif curr_piece.colour == colour:
                break
            else:
                last = [curr_piece]

            left -= 1

        return moves

    '''
    Searches for all valid moves to the right of the chosen piece including possible capture moves.
    It determines what row it will start the search, the row it will stop the search, the direction 
    of the search (i.e. going up to the right or down to the right depending on the colour of the piece), 
    how much it will move along by and keeps a list of all possible capture moves.
    Returns the moves
    '''

    def _search_right(self, start, stop, step, colour, right, captured=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):  # r = row
            if right >= cols:  # right = column
                break

            curr_piece = self.board[r][right]
            if curr_piece == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(r, right)] = last + captured
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        # uses recursion to check if a piece can make a double or triple capture move
                        row = min(r + 3, rows)
                    moves.update(self._search_left(
                        r + step, row, step, colour, right - 1, captured=last))
                    moves.update(self._search_right(
                        r + step, row, step, colour, right + 1, captured=last))
                break
            elif curr_piece.colour == colour:
                break
            else:
                last = [curr_piece]
            right += 1

        return moves
