import pygame
from .constants import white, red, blue, square_size, crown

class Piece:
    padding = 15
    
    def __init__(self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        self.king = False
        self.x = 0
        self.y = 0
        self.pos()

    '''
    Calculates the x and y position based on the row and col the checker piece is in
    '''
    def pos(self):
        self.x = square_size * self.col + square_size // 2
        self.y = square_size * self.row + square_size // 2
    
    '''
    Checks if the checker piece is a king or not.
    '''
    def is_king(self):
        self.king = True
        
    '''
    Draws a normal and king checker pieces. If the pieceis a king it put the crown image on it.
    '''
    def draw_piece(self, win):
        radius = square_size // 2 - self.padding
        pygame.draw.circle(win, self.colour, (self.x, self.y), radius)
        if self.king:
            win.blit(crown, (self.x - crown.get_width() // 2, self.y - crown.get_height() // 2))
    
    '''
    Gets the position of the piece given a set of coordinates and moves it to a new position given a set of coordinates.
    '''
    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.pos()

    '''
    Changes the internal representation of the piece object and returns the colour of the piece as a string.
    '''    
    def __repr__(self):
        return str(self.colour) 