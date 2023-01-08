import pygame, numpy as np, sys
from hexagon import Hexagon

pygame.init()

BACKGROUND = (21,76,121)
TILES = (56,93,56)
HIGHLIGHTEDTILES = (82,97,82)
DESTROYEDTILES = (0,0,0)
SCREENWIDTH = 800
SCREENHEIGHT = 800
BOARDSHAPE = (11,11)

GameRunning = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Trap the Mouse')

board = np.zeros(BOARDSHAPE)
hex1 = Hexagon(100,100,0)

while GameRunning:
    x, y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            GameRunning = False

    clock.tick(60)
    
    screen.fill(BACKGROUND)
    hex1.render(screen)
    pygame.display.update()
    
pygame.quit()