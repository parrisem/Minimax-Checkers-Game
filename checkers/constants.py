import pygame

'''Initialises all the common variables used in all the classes.'''

width, height = 600, 600 # the size of the window
rows, cols = 8, 8 # the size of the checkers board 
square_size = width // cols # the size of each square on the checker board si

# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 128, 0)

# Import images
crown = pygame.transform.scale(pygame.image.load('assets/crown.png'), (34, 25))
rules = pygame.transform.scale(pygame.image.load('assets/rules.png'), (586, 322))
