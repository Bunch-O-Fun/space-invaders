import pygame
import sys
import math

class Display:

    def __init__ (self):

        screen = pygame.display.set_mode((1280,981))
        background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invaders!")
        screen.blit(background,(0,0))


mygame = Display()
running = True

while running:
    pygame.display.flip() #updates the visuals on the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

pygame.quit()
