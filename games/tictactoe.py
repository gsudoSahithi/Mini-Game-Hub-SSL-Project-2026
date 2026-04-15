import pygame
import numpy as np
import time
from game import Game


CELL_SIZE = 60
SIZE = 10
WIN_COUNT = 5
WIDTH = HEIGHT = SIZE * CELL_SIZE


class TicTacToe(Game):
    def __init__(self, p1, p2):
        super().__init__(p1, p2, SIZE, SIZE)

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe 10x10")
    def draw(self):
        self.screen.fill((0, 0, 0))

        for i in range(SIZE):
            pygame.draw.line(self.screen, (200, 200, 200),
                             (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
            pygame.draw.line(self.screen, (200, 200, 200),
                             (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))

        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r, c] == 1:
                    pygame.draw.circle(
                        self.screen,
                        (0, 255, 0),
                        (c * CELL_SIZE + CELL_SIZE // 2,
                         r * CELL_SIZE + CELL_SIZE // 2),
                        20, 2
                    )
                elif self.board[r, c] == -1:
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (c * CELL_SIZE + 10, r * CELL_SIZE + 10),
                                     (c * CELL_SIZE + 50, r * CELL_SIZE + 50), 2)
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (c * CELL_SIZE + 50, r * CELL_SIZE + 10),
                                     (c * CELL_SIZE + 10, r * CELL_SIZE + 50), 2)
    def check_winner(self):
        b = self.board
        windows = np.lib.stride_tricks.sliding_window_view(b, (1, WIN_COUNT))
        sums = windows.sum(axis=-1).squeeze(axis=2)
        if np.any(np.abs(sums) == WIN_COUNT):
            return int(np.sign(sums[np.abs(sums) == WIN_COUNT][0]))
        windows = np.lib.stride_tricks.sliding_window_view(b, (WIN_COUNT, 1))
        sums = windows.sum(axis=-2).squeeze(axis=2)
        if np.any(np.abs(sums) == WIN_COUNT):
            return int(np.sign(sums[np.abs(sums) == WIN_COUNT][0]))
        for i in range(SIZE - WIN_COUNT + 1):
            for j in range(SIZE - WIN_COUNT + 1):
                block = b[i:i+WIN_COUNT, j:j+WIN_COUNT]
                d = np.sum(np.diagonal(block))
                if abs(d) == WIN_COUNT:
                    return int(np.sign(d))
        flipped = np.fliplr(b)
        for i in range(SIZE - WIN_COUNT + 1):
            for j in range(SIZE - WIN_COUNT + 1):
                block = flipped[i:i+WIN_COUNT, j:j+WIN_COUNT]
                d = np.sum(np.diagonal(block))
                if abs(d) == WIN_COUNT:
                    return int(np.sign(d))

        return 0
    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    r, c = y // CELL_SIZE, x // CELL_SIZE

                    if self.board[r, c] == 0:
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
