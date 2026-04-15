import sys
import pygame
import numpy
player1 = sys.argv[1]
player2 = sys.argv[2]
def __init__(self,player1,player2):
    self.player1 = player1
    self.player2 = player2
pygame.init()
screen = pygame.display.set_mode((800,700))
clock = pygame.time.Clock()
surface = pygame.image.load('Game hub photo.jpeg')
