import pygame, numpy as np, sys, math
from hexagon import Hexagon

pygame.init()

BACKGROUND = (21,76,121)
TILES = (56,93,56)
HIGHLIGHTEDTILES = (82,97,82)
DESTROYEDTILES = (0,0,0)
SCREENWIDTH = 800
SCREENHEIGHT = 800
BOARDSHAPE = (11,11)
HEXRADIUS = 30
HEXMINIMALDISTANCE = HEXRADIUS / 2 * math.sqrt(3)

GameRunning = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Trap the Mouse')

board = []
for index1 in  range(11):
    for index2 in range(11):
        if index1 % 2 == 0:
            board.append(Hexagon(100 + index2 * HEXMINIMALDISTANCE * 2, 100 + index1 * 1.5 * HEXRADIUS, 0))
        else:
            board.append(Hexagon(100 + HEXMINIMALDISTANCE + index2 * HEXMINIMALDISTANCE * 2, 100 + 1.5 * HEXRADIUS + (index1 - 1) * 1.5 * HEXRADIUS, 0))

while GameRunning:
    x, y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            GameRunning = False

    clock.tick(60)
    
    screen.fill(BACKGROUND)
    for hex in board:
        hex.render(screen)
        
    pygame.display.update()
    
pygame.quit()