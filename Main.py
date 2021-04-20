# ADD: CODE DOCUMENTATION

import pygame, sys, os, platform
import tkinter as tk
from tkinter import *
from checkers.constants import red, blue, white, black, green, width, height, square_size, rules
from checkers.game import Game
from checkers.button import Button
from minimax.algorithm import minimax
pygame.init()


FPS = 60
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption('Checkers')
font = pygame.font.Font('freesansbold.ttf', 32)
click = False

'''
Renders text and displays it on the window.
'''
def display_message(message):
    while True:

        WIN.fill(black)
        text = font.render(message, 1, white)
        WIN.blit(text, (width / 2 - text.get_width() / 2, height / 3 - text.get_height() / 3))
        
        # Creates the buttons on the main menu.
        new_game_button = Button(white, 50, 300, 200, 50, 'New Game')
        new_game_button.draw(WIN, blue)

        main_menu_button = Button(white, 350, 300, 200, 50, 'Main Menu')
        main_menu_button.draw(WIN, red)

        # Event handling for the end of game menu including buttons. 
        # Checks if the mouse or the close window 'X' was clicked.
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.is_clicked(pos):
                    main()
                elif main_menu_button.is_clicked(pos):
                    main_menu()
                    
        pygame.display.update()

    pygame.quit()

''' 
Displays the main menu of the game.
'''
def main_menu():
    while True:

        WIN.fill(black)
        text = font.render('Main Menu', 1, white)
        WIN.blit(text, (width / 2 - text.get_width() / 2, height / 3 - text.get_height() / 3))

        # Creates the buttons on the main menu.
        start_button = Button(white, 50, 300, 200, 50, 'Start')
        start_button.draw(WIN, blue)

        rules_button = Button(white, 350, 300, 200, 50, 'Rules')
        rules_button.draw(WIN, red)

        # Event handling for the rules menu including buttons. 
        # Checks if the mouse or the close window 'X' was clicked.
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pos):
                    main()
                elif rules_button.is_clicked(pos):
                    rules_menu()

        pygame.display.update()

    pygame.quit()

''' 
Displays the rules of the game.
'''
def rules_menu():
    while True:

        WIN.fill(black)
        title = font.render('Rules', 1, white)

        WIN.blit(title, (width / 2 - title.get_width() / 2, height / 10 - title.get_height() / 6))
        WIN.blit(rules, (width / 2 - rules.get_width() / 2, height / 2 - rules.get_height() / 2))

        # Creates the buttons on the rules menu.
        start_button = Button(white, 50, 540, 200, 50, 'Start')
        start_button.draw(WIN, blue)

        main_menu_button = Button(white, 350, 540, 200, 50, 'Main Menu')
        main_menu_button.draw(WIN, red)

        # Event handling for the rules menu including buttons. 
        # Checks if the mouse or the close window 'X' was clicked.
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pos):
                    main()
                elif main_menu_button.is_clicked(pos):
                    main_menu()

        pygame.display.update()

    pygame.quit()

'''
Gets the position of the mouse in the checkers game and returns the row and col of the mouse.
'''
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // square_size
    col = x // square_size
    return row, col

''' 
Runs the checkers game and generates the AI moves using the minimax algorithm.
'''
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == red: # change_turn
            value, new_board = minimax(game.get_board(), 3, red, game)
            game.ai_move(new_board)

        # gets the colour returned from winner() in the game class
        # returns a message stating the winner of the game 
        if game.winner() == red:
            display_message('RED WON!')
        elif game.winner() == blue:
            display_message('BLUE WON!')
            run = False

        # event handling for the checkers game. Checks if the mouse or the close window 'X' was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.choose_piece(row, col)

        game.update()     

    pygame.quit()


'''
In this function I tried to create a menu bar using tkinter and embed a pygame window into it. 
'''
def menu_bar():
    root = tk.Tk() # main window
    root.title('Checkers')
    frame = tk.Frame(root, width = 200, height = 200) # tkinter frame
    py_frame = tk.Frame(root, width = width, height = height) # pygame frame
    menu_bar = Menu(root)
    root.config(menu = menu_bar)
    # create menu items
    option_menu = Menu(menu_bar)
    menu_bar.add_cascade(label = 'Options', menu = option_menu)
    option_menu.add_command(label = 'Menu', command = main_menu)
    option_menu.add_command(label = 'Rules', command = rules_menu)
    option_menu.add_command(label = 'Quit Game', command = root.quit)
    # packing
    frame.pack(expand = True)
    frame.pack_propagate(0)
    py_frame.pack(side = 'left')
    #embed.pack()

    # embeds pygame window
    os.environ['SDL_WINDOWID'] = str(py_frame.winfo_id())
    system = platform.system()
    if system == 'Windows':
        os.environ['SDL_VIDEODRIVER'] = 'windib'
    elif system == "Linux":
            os.environ['SDL_VIDEODRIVER'] = 'x11'

    root.update_idletasks()
    pygame.init()
    #root.after(main_menu())
    #main_menu()


    root.mainloop()
#menu_bar()

main_menu()