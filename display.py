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

class Player:

    def __init__(self,xpos,ypos):
        global x
        x = 640
        global y 
        y = 890
        self.x = x
        self.y = y
        GREEN = (54,223,42)
        global playerimg
        playerimg = pygame.Rect(x,y,30,30)
        pygame.draw.rect(screen,GREEN,playerimg,0) #current player is a square, add graphics later on

    def player_action(self,x,y):
        self.x = x
        self.y = y
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_LEFT]:
            x -= 15
        if key_press[pygame.K_RIGHT]:
            x += 15
        playerimg = pygame.Rect(x,y,30,30) #reestablish the rectangle with the next x coordinate
        screen.blit(background,(0,0)) #redraws the background
        pygame.draw.rect(screen,(52,223,42),playerimg,0) #redraws the square with its new position
        pygame.display.flip() #updates the screen with all changes


mygame = Display()
playership = Player(640,890)

running = True

while running:
    pygame.display.flip() #updates the visuals on the screen
    pygame.display.update()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            playership.player_action(x,y)



        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

pygame.quit()
