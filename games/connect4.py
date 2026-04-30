import pygame
import numpy as np
import os
import sys
import subprocess
curr_path=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_path,".."))

from baseclass import Game

SIZE=7
# Handles board drawing, player moves, and winner detection
class Connect4(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2, rows=SIZE, cols=SIZE)
        # Size of each cell based on screen dimensions
        self.cell_size = min(self.width // self.cols, self.height // self.rows)
        pygame.display.set_caption("Connect4")
    def draw(self):
        # Draw top black bar (for UI space)
        pygame.draw.rect(self.screen,(0,0,0),(0,0,self.width,self.cell_size))

        for r in range(self.rows):
            for c in range(self.cols):
                # Position of each cell
                x = c * self.cell_size
                y = (r + 1) * self.cell_size

                pygame.draw.rect(self.screen,'#441462', (x, y, self.cell_size, self.cell_size))
                # Center of circle inside cell
                center = (x + self.cell_size//2, y + self.cell_size//2)

                val = self.board[r][c]
                 # Choose color based on player
                color = (10,10,10) if val == 0 else ('#BBA8C0' if val == 1 else '#DD6C92')
                radius = self.cell_size//2 - (5 if val == 0 else 8)

                pygame.draw.circle(self.screen, color, center, radius)

    def drop_piece(self, col):
        # Place piece in lowest empty row
        for r in range(self.rows-1, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = self.get_symbol()
                return True
        # Column is full
        return False
    def check_winner(self):
        sym=self.get_symbol()
        b=(self.board==sym)
        # Check horizontal 4 in a row
        if np.any(b[:,:-3]&b[:,1:-2]&b[:,2:-1]&b[:,3:]): return sym
        # Check vertical 4 in a row
        if np.any(b[:-3,:]&b[1:-2,:]&b[2:-1,:]&b[3:,:]): return sym
        # Check diagonal (top-left to bottom-right)
        if np.any(b[:-3,:-3]&b[1:-2,1:-2]&b[2:-1,2:-1]&b[3:,3:]): return sym
        # Check diagonal (bottom-left to top-right)
        if np.any(b[3:,:-3]&b[2:-1,1:-2]&b[1:-2,2:-1]&b[:-3,3:]): return sym
        # Check draw (no empty spaces)
        if not np.any(self.board==0): return 3
        return 0
    def run(self):
        clock = pygame.time.Clock()
        mouse_x = 0

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                # Close game window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Track mouse movement for hover effect
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x = event.pos[0]
                # When player clicks to drop a piece
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // self.cell_size

                    if self.drop_piece(col):
                        winner = self.check_winner()
#Deciding winner and loser names
                        if winner != 0:
                            # Handles draw case
                            if winner ==3:
                                win_name="draw"
                                los_name="draw"
                            else:
                                win_name=self.get_current_player()
                                los_name=self.players[1 - self.current_turn]
#Storing result into history.csv                               
                            self.store_result(win_name, los_name, "Connect4")
                            self.draw()
                            self.show_result(winner if winner != 3 else 0)
                            sort_type=self.sort_metric()
                            subprocess.run(f"bash ./leaderboard.sh {sort_type}",shell=True)
                            self.call_visualization()
                            return
                    #switch to next player
                        self.switch_turn()

            self.draw()
            #hover coin
            color = '#BBA8C0' if self.get_symbol()==1 else '#DD6C92'
            pygame.draw.circle(self.screen, color,
                            (mouse_x, self.cell_size//2),
                            self.cell_size//2 - 5)

            pygame.display.update()
if __name__ == "__main__":
    game = Connect4("P1", "P2")
    game.run()
