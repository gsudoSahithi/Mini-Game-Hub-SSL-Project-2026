import pygame
import numpy as np
import time
from .baseclass import Game
SIZE = 10
WIN_COUNT = 5

class TicTacToe(Game):
    def __init__(self, p1, p2):
        super().__init__(p1, p2, SIZE, SIZE)
        pygame.display.set_caption("Tic-Tac-Toe")

    def draw_pieces(self):
        for r in range(self.rows):
            for c in range(self.cols):
                center_x = c * self.cell_size + self.cell_size // 2
                center_y = r * self.cell_size + self.cell_size // 2

                if self.board[r, c] == 1:
                    pygame.draw.circle(self.screen, (255, 0, 255),
                                       (center_x, center_y), 20, 2)

                elif self.board[r, c] == -1:
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (center_x - 15, center_y - 15),
                                     (center_x + 15, center_y + 15), 2)
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (center_x + 15, center_y - 15),
                                     (center_x - 15, center_y + 15), 2)

    def check_winner(self):
        b = self.board
        k = WIN_COUNT

        # Horizontal
        h = np.lib.stride_tricks.sliding_window_view(b, (1, k))
        h_sum = h.sum(axis=-1).squeeze(axis=2)
        if np.any(h_sum == k):
            return 1
        if np.any(h_sum == -k):
            return -1

        # Vertical
        v = np.lib.stride_tricks.sliding_window_view(b, (k, 1))
        v_sum = v.sum(axis=-2).squeeze(axis=2)
        if np.any(v_sum == k):
            return 1
        if np.any(v_sum == -k):
            return -1

        # Diagonal
        d = np.lib.stride_tricks.sliding_window_view(b, (k, k))
        diag = np.diagonal(d, axis1=2, axis2=3).sum(axis=-1)
        if np.any(diag == k):
            return 1
        if np.any(diag == -k):
            return -1

        # Anti-diagonal
        flipped = np.fliplr(b)
        ad = np.lib.stride_tricks.sliding_window_view(flipped, (k, k))
        anti = np.diagonal(ad, axis1=2, axis2=3).sum(axis=-1)
        if np.any(anti == k):
            return 1
        if np.any(anti == -k):
            return -1

        return 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    r, c = y // self.cell_size, x // self.cell_size

                    if r < self.rows and c < self.cols and self.board[r, c] == 0:
                        self.board[r, c] = self.get_symbol()

                        winner = self.check_winner()
                        if winner != 0:
                            self.draw()
                            pygame.display.update()
                            time.sleep(1)
                            return self.players[0] if winner == 1 else self.players[1]

                        self.switch_turn()

            self.draw()
            pygame.display.update()
