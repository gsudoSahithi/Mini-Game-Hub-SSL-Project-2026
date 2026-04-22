import pygame
import numpy as np

class Game:
    def __init__(self, player1, player2, rows, cols):
        pygame.init()
        self.players = [player1, player2]
        self.cols = cols
        self.rows = rows
        self.current_turn = 0
        self.board = np.zeros((rows, cols), dtype=int)
        self.cell_size = 60
        self.screen = pygame.display.set_mode(
            (cols * self.cell_size, rows * self.cell_size)
        )

    def get_current_player(self):
        return self.players[self.current_turn]

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def get_symbol(self):
        return 1 if self.current_turn == 0 else -1

    def draw_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(self.screen, (0, 200, 255),
                             (0, i * self.cell_size),
                             (self.cols * self.cell_size, i * self.cell_size))

        for j in range(self.cols + 1):
            pygame.draw.line(self.screen, (0, 200, 255),
                             (j * self.cell_size, 0),
                             (j * self.cell_size, self.rows * self.cell_size))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_pieces()

    def draw_pieces(self):
        pass
