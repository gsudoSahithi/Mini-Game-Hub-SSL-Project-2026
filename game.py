import sys
import numpy as np
import pygame
import numpy as np
from games import tictactoe
from games import othello
from games import connect4

class Game:
    def __init__(self, player1, player2, rows, cols):
        pygame.init()
        self.players = [player1, player2]
        self.cols=cols
        self.rows=rows
        self.current_turn = 0
        self.board = np.zeros((rows,cols), dtype=int)
        self.cell_size = 60
        self.screen = pygame.display.set_mode((cols * self.cell_size, rows * self.cell_size))

    def get_current_player(self):
        return self.players[self.current_turn]

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def get_symbol(self):
       return 1 if self.current_turn == 0 else -1

    def draw_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(self.screen, (0,200,255),
                         (0, i * self.cell_size),
                         (self.cols * self.cell_size, i * self.cell_size))

        for j in range(self.cols + 1):
            pygame.draw.line(self.screen, (0,200,255),
                         (j * self.cell_size, 0),
                         (j * self.cell_size, self.rows * self.cell_size))
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_pieces()   

    def draw_pieces(self):
        pass

    def check_winner(self):
        pass

    def run(self):
        pass
pygame.init()
screen = pygame.display.set_mode((600,600))
surface = pygame.image.load('mini_game_hub_600x600.png')
tictactoe_rect = pygame.Rect(45, 188, 232, 163)
othello_rect = pygame.Rect(322, 188, 232, 163)
connect4_rect = pygame.Rect(172, 377, 255, 163)
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
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
