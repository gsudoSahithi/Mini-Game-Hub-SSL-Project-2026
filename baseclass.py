import pygame
import numpy as np
import time
import subprocess

# Base Game class used by all games (Connect4, TicTacToe, Othello)
# Contains common logic like turn handling, board setup, result storage, and UI utilities
class Game:
    def __init__(self, player1, player2, rows, cols):

        pygame.init()

        #Stores player names
        self.players = [player1, player2]

        #Board size
        self.cols = cols
        self.rows = rows

        #Finding which player is playing
        self.current_turn = 0

        #Creates empty game board
        self.board = np.zeros((rows, cols), dtype=int)

        self.width = 600
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.sort_option = "wins"

    #Returns name of current player
    def get_current_player(self):
        return self.players[self.current_turn]

    #Switches turns between players
    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    #Return symbol for current player (1 or -1)
    def get_symbol(self):
        return 1 if self.current_turn == 0 else -1

    #Basic drawing function
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_pieces()
    def draw_pieces(self):
        pass

    # Store match result in history.csv file
    def store_result(self, winner, loser, game):
        date = time.strftime("%Y-%m-%d", time.localtime())

        with open("history.csv", "a") as file:
            file.write(f"{winner},{loser},{date},{game}\n")

    #Calls external visualization script for stats display
    def call_visualization(self):
        subprocess.run(["python", "games/visualization.py"])

    #Show game result screen 
    def show_result(self, winner):

        font = pygame.font.SysFont(None, 48)

        if winner == 1:
            text = font.render(f"{self.players[0]} wins!", True, (255, 255, 255))
        elif winner == -1:
            text = font.render(f"{self.players[1]} wins!", True, (255, 255, 255))
        else:
            text = font.render("It's a draw!", True, (255, 255, 255))

        #Center text on screen
        rect = text.get_rect(center=(self.width // 2, self.height // 2))

        self.screen.blit(text, rect)
        pygame.display.update()

        #Pausing the result
        pygame.time.delay(2000)
    def layout(self, screen):

        screen_w, screen_h = 600, 700

        popup_w, popup_h = 420, 380
        btn_w, btn_h = 360, 55

        popup_x = (screen_w - popup_w) // 2
        popup_y = (screen_h - popup_h) // 2

        popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

        pygame.draw.rect(screen, (20, 20, 20), popup_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2, border_radius=15)

        #Defines button positions
        h_rect = pygame.Rect(popup_x + (popup_w - btn_w) // 2, popup_y + 15, btn_w, btn_h)
        wins_rect = pygame.Rect(popup_x + (popup_w - btn_w) // 2, popup_y + 85, btn_w, btn_h)
        loss_rect = pygame.Rect(popup_x + (popup_w - btn_w) // 2, popup_y + 155, btn_w, btn_h)
        ratio_rect = pygame.Rect(popup_x + (popup_w - btn_w) // 2, popup_y + 225, btn_w, btn_h)

        font = pygame.font.SysFont("segoeui", 24, bold=True)

        #Draws buttons
        for rect, text in [
            (h_rect, "Sort Leaderboard by?"),
            (wins_rect, "By Wins"),
            (loss_rect, "By Losses"),
            (ratio_rect, "By W/L Ratio")
        ]:
            pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)

            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=rect.center))

        return h_rect, wins_rect, loss_rect, ratio_rect

    def sort_metric(self):

        while True:

            self.screen.fill((30, 30, 30))

            #Draw popup UI
            h_rect, wins_rect, loss_rect, ratio_rect = self.layout(self.screen)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    #Returns the selected sorting option
                    if wins_rect.collidepoint(event.pos):
                        return "wins"
                    if loss_rect.collidepoint(event.pos):
                        return "loss"
                    if ratio_rect.collidepoint(event.pos):
                        return "ratio"

            pygame.display.update()
