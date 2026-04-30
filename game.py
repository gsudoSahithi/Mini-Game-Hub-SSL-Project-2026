import sys
import pygame
import numpy as np
from games import tictactoe
from games import othello
from games import connect4
pygame.init()
screen = pygame.display.set_mode((600,700))
surface = pygame.image.load('mini_game_hub_exact_600x700.png')
surface = pygame.transform.scale(surface,(600,700))
#Tic Tac Toe(left top)
tictactoe_rect = pygame.Rect(45, 180, 232, 160)

#Othello(right top)
othello_rect = pygame.Rect(323, 180, 232, 160)

#Connect4(center bottom)
connect4_rect = pygame.Rect(172, 370, 255, 160)

def post_game_screen(screen):
    font = pygame.font.Font(None, 60)
    width, height = screen.get_size()
    # Load and scale background image
    bg = pygame.image.load("post_game.png")
    bg = pygame.transform.scale(bg, (width, height))

    # CENTER EVERYTHING TOGETHER
    center_y = height // 2

    # Title (slightly above center)
    title = font.render("Play Again?", True, (255, 255, 255))
    title_rect = title.get_rect(center=(width // 2, center_y - 80))

    # Button sizes
    button_width = width // 4
    button_height = height // 10

    gap = width // 20   # dynamic gap (better scaling)

    # Buttons centered horizontally
    total_width = button_width * 2 + gap
    start_x = (width - total_width) // 2

    yes_button = pygame.Rect(start_x, center_y, button_width, button_height)
    no_button = pygame.Rect(start_x + button_width + gap, center_y, button_width, button_height)

    while True:
        screen.blit(bg, (0, 0))

        # Title
        screen.blit(title, title_rect)

        # Buttons
        pygame.draw.rect(screen, (0, 200, 0), yes_button, border_radius=10)
        pygame.draw.rect(screen, (200, 0, 0), no_button, border_radius=10)

        # Button text (perfectly centered)
        yes_text = font.render("Yes", True, (255, 255, 255))
        no_text = font.render("No", True, (255, 255, 255))

        screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))
        screen.blit(no_text, no_text.get_rect(center=no_button.center))

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return True
                if no_button.collidepoint(event.pos):
                    return False
running=True
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #Detecting mouse position and executing game according to it
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if tictactoe_rect.collidepoint(mouse_pos):
                game = tictactoe.TicTacToe(sys.argv[1],sys.argv[2])
                game.run()
                if not post_game_screen(screen):
                    running = False

            if othello_rect.collidepoint(mouse_pos):
                game = othello.Othello(sys.argv[1], sys.argv[2])
                game.run()
                if not post_game_screen(screen):
                    running = False
                    
            if connect4_rect.collidepoint(mouse_pos):
                game = connect4.Connect4(sys.argv[1],sys.argv[2])
                game.run()
                if not post_game_screen(screen):
                    running = False
    screen.blit(surface,(0,0))
    pygame.display.update()
