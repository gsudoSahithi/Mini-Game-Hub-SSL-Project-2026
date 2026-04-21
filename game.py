import sys
import numpy as np
import pygame
from games import tictactoe
from games import othello
from games import connect4
import numpy as np
class Game:
    def __init__(self, player1, player2, rows, cols):
        self.players = [player1, player2]
        self.current_turn = 0
        self.board = np.zeros((rows,cols), dtype=int)

    def get_current_player(self):
        return self.players[self.current_turn]

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def draw_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(self.screen, (200, 200, 200),
                         (0, i * self.cell_size),
                         (self.cols * self.cell_size, i * self.cell_size))

        for j in range(self.cols + 1):
            pygame.draw.line(self.screen, (200, 200, 200),
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
screen = pygame.display.set_mode((800,700))
surface = pygame.image.load('mini_game_hub_800x700.png')
tictactoe_rect = pygame.Rect(60, 220, 310, 190)
othello_rect = pygame.Rect(430,220,310,190)
connect4_rect = pygame.Rect(230,440,340,190)
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if tictactoe_rect.collidepoint(mouse_pos):
                tictactoe.run()
            if othello_rect.collidepoint(mouse_pos):
                othello.run()
            if connect4_rect.collidepoint(mouse_pos):
                connect4.run()
    screen.blit(surface,(0,0))
    pygame.display.update()
