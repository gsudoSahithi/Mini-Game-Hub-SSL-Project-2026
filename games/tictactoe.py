import pygame
import numpy as np
import os
import sys
import subprocess
curr_path=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_path,".."))

from baseclass import Game

SIZE=10
#grid drawing, player moves, and winner detection
class TicTacToe(Game):
    def __init__(self, p1, p2):
        super().__init__(p1, p2, rows=SIZE, cols=SIZE)
        pygame.display.set_caption("Tic-Tac-Toe")
        self.cell_size = min(self.width // self.cols, self.height // self.rows)
        #Vertical offset to shift board down (for UI space)
        self.offset_y=100
         #Loading and resizing background image
        self.background = pygame.image.load("Tic Tac Toe.jpeg")
        self.background = pygame.transform.scale(self.background,(600,700))

    def draw_grid(self):
        self.screen.blit(self.background,(0,0))
        #Draw horizontal grid lines
        for i in range(self.rows + 1):
            pygame.draw.line(self.screen,(0,200,255),(0,self.offset_y+i*self.cell_size),(self.cols*self.cell_size,self.offset_y+i*self.cell_size))
        #Draw vertical grid lines
        for j in range(self.cols + 1):
            pygame.draw.line(self.screen,(0,200,255),(j*self.cell_size,self.offset_y),(j*self.cell_size,self.offset_y+self.rows*self.cell_size))

    def draw_pieces(self):
        #Draw X and O based on board values
        for r in range(self.rows):
            for c in range(self.cols):
                # FIXED POSITION
                x = c * self.cell_size + self.cell_size // 2
                y = self.offset_y + r * self.cell_size + self.cell_size // 2

                radius = self.cell_size // 3
                offset = self.cell_size // 4
                # Draw O for player 1
                if self.board[r,c]==1:
                    pygame.draw.circle(self.screen, (255,0,255), (x,y), radius, 2)
                # Draw X for player -1
                elif self.board[r,c]==-1:
                    pygame.draw.line(self.screen, (255,0,0),(x-offset,y-offset),(x+offset,y+offset),2)
                    pygame.draw.line(self.screen, (255,0,0),(x+offset,y-offset),(x-offset,y+offset),2)

    def check_winner(self):
        s,b = self.get_symbol(), self.board==self.get_symbol()
        #Check horizontal 5 in a row
        if np.any(b[:,:-4]&b[:,1:-3]&b[:,2:-2]&b[:,3:-1]&b[:,4:]): return s
        #Check vetical 5 in a row
        if np.any(b[:-4,:]&b[1:-3,:]&b[2:-2,:]&b[3:-1,:]&b[4:,:]): return s
        #Check diagonal 5 in a row from top left to bottom right
        if np.any(b[:-4,:-4]&b[1:-3,1:-3]&b[2:-2,2:-2]&b[3:-1,3:-1]&b[4:,4:]): return s
        #Check diagonal 5 in a row from bottom left to top right
        if np.any(b[4:,:-4]&b[3:-1,1:-3]&b[2:-2,2:-2]&b[1:-3,3:-1]&b[:-4,4:]): return s
        return 3 if not np.any(self.board==0) else 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # FIXED POSITION
                    row = (y - self.offset_y) // self.cell_size
                    col = x // self.cell_size

                    if row < self.rows and col < self.cols and self.board[row, col] == 0:
                        self.board[row, col] = self.get_symbol()
                        winner = self.check_winner()
#Deciding winner and loser names
                        if winner != 0:
                            if winner ==3:
                                win_name="draw"
                                los_name="draw"
                            else:
                                win_name=self.get_current_player()
                                los_name=self.players[1 - self.current_turn]
                        #Storing result into history.csv                               
                            self.store_result(win_name, los_name, "TicTacToe")
                            self.draw()
                            self.show_result(winner if winner != 3 else 0)
                            sort_type=self.sort_metric()
                            subprocess.run(f"bash ./leaderboard.sh {sort_type}", shell=True)
                            self.call_visualization()
                            return
                        self.switch_turn()
            self.draw()
            pygame.display.update()

if __name__=="__main__":
    TicTacToe("P1","P2").run()
