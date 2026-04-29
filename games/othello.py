import pygame
import numpy as np
from baseclass import Game
import subprocess
pygame.init()

class Othello(Game):
    def __init__(self,pl1,pl2):
        super().__init__(pl1,pl2,rows=8,cols=8)
        screen_width = 600
        screen_height = 700
        self.cell_size = int(min((screen_width * 0.60) // self.cols,(screen_height * 0.70) // self.rows))
        self.screen = pygame.display.set_mode((600,700))
        self.background = pygame.image.load("Othello background.jpeg")
        self.background = pygame.transform.scale(self.background,(600,700))
        #Track current player for UI highlight
        self.glow = self.current_turn
        #Initial 4 center pieces
        self.board[3][3]=1
        self.board[3][4]=-1
        self.board[4][3]=-1
        self.board[4][4]=1
        pygame.display.set_caption("Othello")

    def othello_grid(self):
        #Defining board area
        board_width  = self.cols * self.cell_size
        board_height = self.rows * self.cell_size
        left_margin  = int(0.20 * 600)
        top_margin    = int(0.14 * 700)
        #Draw horizontal grid lines
        for r in range(self.rows + 1):
            y = top_margin + r * self.cell_size
            pygame.draw.line(self.screen,(0,0,0),(left_margin, y),(left_margin + board_width, y),2)
        #Draw vertical grid lines
        for c in range(self.cols + 1):
            x = left_margin + c * self.cell_size
            pygame.draw.line(self.screen,(0,0,0),(x,top_margin),(x,top_margin+board_height),2)

    def draw_circle(self):
        #Convert board values into black/white discs
        left_margin  = int(0.20 * 600)
        top_margin    = int(0.14 * 700)
        for r in range(self.rows):
            for c in range(self.cols):
                #Converting grid positions to coordinates
                x = left_margin + c*self.cell_size + self.cell_size // 2
                y = top_margin + r*self.cell_size + self.cell_size // 2
                radius = self.cell_size // 3
                #Black disc
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, (0,0,0), (x,y), radius)
                #White disc
                elif self.board[r][c] == -1:
                    pygame.draw.circle(self.screen, (255,255,255), (x,y) ,radius)

    def highlight(self):
        #Highlighting border according to player's turn
        left_margin  = int(0.20 * 600)
        right_margin = int(0.20 * 600)
        self.left_panel = pygame.Rect(0,0,left_margin-24,self.height)
        self.right_panel = pygame.Rect(self.width - right_margin+24,0,right_margin,self.height)
        if self.glow==0:
            pygame.draw.rect(self.screen,(255,255,0),self.left_panel,3)
        if self.glow==1:
            pygame.draw.rect(self.screen,(255,255,0),self.right_panel,3)

    def valid_move(self,row,col):
        #Checking if move is legal
        player = self.get_symbol()
        other = -player

        if self.board[row][col] != 0:
            return False
        #All 8 grid directions possible from a given grid
        directions = [(-1,0), (1,0), (0,-1), (0,1),(-1,-1), (-1,1), (1,-1), (1,1)]

        for r,c in directions:
            ro = row+r
            co = col+c
            count = 0

            while 0<=ro<self.rows and 0<=co<self.cols:
                if self.board[ro][co] == other:
                    count += 1
                elif self.board[ro][co] == player:
                    if count > 0:
                        return True
                    break
                else:
                    break
                ro += r
                co += c

        return False

    def change_color(self,row,col):
        #Finding discs whose colour should be changed 
        player = self.get_symbol()
        other = -player
        change=[]
        directions = [(-1,0), (1,0), (0,-1), (0,1),(-1,-1), (-1,1), (1,-1), (1,1)]

        for r,c in directions:
            ro = row+r
            co = col+c
            temp=[]

            while 0<=ro<self.rows and 0<=co<self.cols:
                if self.board[ro][co] == other:
                    temp.append((ro,co))
                elif self.board[ro][co] == player:
                    if len(temp) > 0:
                        change += temp
                    break
                else:
                    break
                ro += r
                co += c

        return change

    def exec(self,row,col):
        #Executing Valid Moves
        if not self.valid_move(row, col):
            return False

        player = self.get_symbol()
        change = self.change_color(row, col)

        self.board[row][col] = player

        for r, c in change:
            self.board[r][c] = player

        return True
    def draw_score(self):
        font = pygame.font.Font(None, 50)

        # count pieces
        black_score = np.sum(self.board == 1)
        white_score = np.sum(self.board == -1)

        # render text
        black_text = font.render(str(black_score).zfill(2), True, (255, 255, 255))
        white_text = font.render(str(white_score).zfill(2), True, (255, 255, 255))

        # positions (adjust slightly if needed)
        left_x = 45
        left_y = 350

        right_x = 555
        right_y = 350

        # center text properly
        self.screen.blit(black_text, black_text.get_rect(center=(left_x, left_y)))
        self.screen.blit(white_text, white_text.get_rect(center=(right_x, right_y)))
    def check_game_over(self):

        # check if board is full
        if not np.any(self.board == 0):
            return True

        # check if any valid move exists for BOTH players
        for r in range(self.rows):
            for c in range(self.cols):

                if self.board[r][c] == 0:

                    # check for player 1
                    self.current_turn = 0
                    if self.valid_move(r, c):
                        return False

                    # check for player 2
                    self.current_turn = 1
                    if self.valid_move(r, c):
                        return False

        return True
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.othello_grid()
        self.draw_circle()
        self.highlight()
        self.draw_score()
        pygame.display.update()
    
    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    left_margin  = int(0.20 * 600)
                    top_margin    = int(0.14 * 700)

                    row = int((y-top_margin)// self.cell_size)
                    col = int((x-left_margin)// self.cell_size)

                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        if self.exec(row, col):
                            self.switch_turn()
                            self.glow = self.current_turn

            self.draw()
            self.draw()

        # check game over
        #winning conditions
        if self.check_game_over():

            black = np.sum(self.board == 1)
            white = np.sum(self.board == -1)

            if black > white:
                winner = 1
            elif white > black:
                winner = -1
            else:
                winner = 3
            if winner != 0:
                if winner ==3:
                    win_name="draw"
                    los_name="draw"
                else:
                    win_name=self.get_current_player()
                    los_name=self.players[1 - self.current_turn]
#Storing result into history.csv                               
                    self.store_result(win_name, los_name, "Othello")
                    self.draw()
                    self.show_result(winner if winner != 3 else 0)
                    sort_type=self.sort_metric()
                    subprocess.run(f"bash ./leaderboard.sh {sort_type}",shell=True)
                    self.call_leaderboard(sort_type)
                    self.call_visualization()
                    return
        has_move = False

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0 and self.valid_move(r, c):
                    has_move = True
                    break
            if has_move:
                break
        if not has_move:
            black = np.sum(self.board == 1)
            white = np.sum(self.board == -1)

            if black > white:
                winner = 1
            elif white > black:
                winner = -1
            else:
                winner = 3
            if winner != 0:
                if winner ==3:
                    win_name="draw"
                    los_name="draw"
                else:
                    win_name=self.get_current_player()
                    los_name=self.players[1 - self.current_turn]
#Storing result into history.csv                               
                    self.store_result(win_name, los_name, "Othello")
                    self.draw()
                    self.show_result(winner if winner != 3 else 0)
                    sort_type=self.sort_metric()
                    subprocess.run(f"bash ./leaderboard.sh {sort_type}",shell=True)
                    self.call_visualization()
                    return
if __name__ == "__main__":
    game = Othello("P1", "P2")
    game.run()
