import pygame
import sys

BACKGROUND = (21,76,121)
CarryOn = True

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Trap the Mouse')

while CarryOn:
    screen.fill(BACKGROUND)
    x, y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            CarryOn = False

    clock.tick(60)
    
    pygame.display.update()
    
pygame.quit()