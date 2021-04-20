import pygame


class Button():
    def __init__(self, colour, row, col, width, height, text=''):
        self.colour = colour
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.text = text
    '''
    Draws a button on the window
    '''

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.row - 2,
                                            self.col - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.colour, (self.row,
                                            self.col, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('freesansbold.ttf', 18)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.row + (self.width / 2 - text.get_width() / 2),
                            self.col + (self.height / 2 - text.get_height() / 2)))

    '''
    Gets the position of the mouse
    '''

    def is_clicked(self, pos):
        if pos[0] > self.row and pos[0] < self.row + self.width:
            if pos[1] > self.col and pos[1] < self.col + self.height:
                return True

        return False
