import pygame
import sys
import math

class Display:

    def __init__ (self):

        pygame.init()
        global screen
        screen = pygame.display.set_mode((1280,981))
        self.screen = screen
        global background
        background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invaders!")
        screen.blit(background,(0,0))


    def player(self,x,y):

        GREEN = (54,223,42)
        self.x = x
        self.y = y
        global playerimg
        playerimg = pygame.Rect(x,y,30,30)
        pygame.draw.rect(screen,GREEN,playerimg,0) #current player is a square, add graphics later on


    def player_move(self,x,y):
        self.x = x
        self.y = y
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 15
                print("left")
            if event.key == pygame.K_RIGHT:
                x += 15
                print("right")
        playerimg.move_ip(x,y)
        pygame.display.flip()
        pygame.display.update()



mygame = Display()
mygame.player(640,890)
running = True

while running:
    pygame.display.flip() #updates the visuals on the screen
    pygame.display.update()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            mygame.player_move(640,890)

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

pygame.quit()
