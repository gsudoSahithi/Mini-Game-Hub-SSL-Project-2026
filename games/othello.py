import sys
import numpy as np
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
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #Detecting mouse position and executing game according to it
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if tictactoe_rect.collidepoint(mouse_pos):
                game = tictactoe.TicTacToe("Player 1", "Player 2")
                game.run()

            if othello_rect.collidepoint(mouse_pos):
                game = othello.Othello("Player 1", "Player 2")
                game.run()
            if connect4_rect.collidepoint(mouse_pos):
                game = connect4.Connect4("Player 1", "Player 2")
                game.run()
    screen.blit(surface,(0,0))
    pygame.display.update()
