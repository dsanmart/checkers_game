import pygame
from constants import *
from game import Game
from algorithm import minimax
from menu import Menu

# Frames per Second for the while loops
FPS = 60

menu_font = '8-BIT_WONDER.TTF' # Load font

WIN = pygame.display.set_mode((width, height))

global difficulty_level 
difficulty_level = 1


def welcome(): # Draw main menu. Run-time complexity of O(1). The run-time is always constant, as will be for the loading of the screens below.
    run = True
    clock = pygame.time.Clock()
    m = Menu(WIN)
    pygame.display.set_caption('Main Menu')
    while run:
        clock.tick(FPS)
        m.draw_menu()
        value = m.check_events() # when pressed enter inside check_events() it will return the selected option

        if value == "START GAME":
            main()
        elif value == "DIFFICULTY":
            welcome_difficulty() # Screen to change depth of the tree on the AI
        elif value == "CREDITS":
            welcome_credits()
        elif value == "QUIT":
            run = False

        pygame.display.update()

def welcome_credits(): # Draw credits screen and wait for backspace to be pressed to go back. Run-time complexity of O(1)
    run = True
    clock = pygame.time.Clock()
    m = Menu(WIN)
    pygame.display.set_caption('Credits')
    while run:
        m.draw_credits()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                run = False
                welcome()

        pygame.display.update()

def welcome_difficulty(): # Screen in the main manu to set difficulty level of the AI. Run-time complexity of O(1)
    run = True
    clock = pygame.time.Clock()
    m = Menu(WIN)
    pygame.display.set_caption('Difficulty')
    global difficulty_level
    initdif = difficulty_level # Set initial difficulty when the screen was called to use it when backspace is pressed
    currentdif = initdif
    while run:
        clock.tick(FPS)
        m.draw_difficulty(currentdif)
        currentdif = m.check_events_difficulty(initdif, currentdif)
        if currentdif > 100: # This is used to detect wether backspace or return keys were pressed
            currentdif -= 100 # This reverts the value to its correct one
            run = False
        pygame.display.update()
    difficulty_level = currentdif # Set global variable with the selected difficulty

def get_pos_mouse(pos): # Run-time complexity of O(1)
    # get position of mouse
    x, y = pos
    row = y // square_size
    col = x // square_size
    return row, col

# main function for the game. Run-time complexity of O(N), where N are the moves made by the player.
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    pygame.display.set_caption('Checkers')

    while run:
        clock.tick(FPS)

        if game.turn == white:
            value, new_board = minimax(game.get_board(), difficulty_level, -10000, 10000, white, game)
            game.ai_move(new_board)
            
        if game.winner() != None:
            winner = game.winner()
            draw_winner(winner)
            run = False

        # check if any event has taken place, if so they will be in even.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # clicking on piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_mouse(pos)
                game.select(row, col)

        game.update()

def draw_winner(winner): # Draw screen showing the winner of the game. Run-time complexiy of O(1)
    run = True
    clock = pygame.time.Clock()
    m = Menu(WIN)
    pygame.display.set_caption('GAME OVER')
    while run:
        m.draw_winner(winner, difficulty_level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    
    pygame.quit()
   

welcome()
