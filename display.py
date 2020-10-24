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
        self.x = x
        self.y = y
        GREEN = (54,223,42)
        global playerimg
        playerimg = pygame.Rect(x,y,30,30)
        pygame.draw.rect(screen,GREEN,playerimg,0) #current player is a square, add graphics later on

    def movement(self,x): # this function actually lets me change the value of x so the blits don't reset the player to the intial position
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_LEFT]: #if left key is pressed, move 15 pixels left
            if x >= 85:
                x -= 15
            print("left")
        if key_press[pygame.K_RIGHT]: #if right key is pressed, move 15 pixels right
            if x <= 1195:
                x += 15
            print("right")
        return x

    def player_action(self,x,y):
        self.x = x
        self.y = y
        playerimg = pygame.Rect(x,y,30,30) #reestablish the rectangle with the next x coordinate
        screen.blit(background,(0,0)) #redraws the background
        pygame.draw.rect(screen,(52,223,42),playerimg,0) #redraws the square with its new position
        pygame.display.flip() #updates the screen with all changes

mygame = Display()
x = 640
y = 890
playership = Player(x,y)
running = True
while running:
    pygame.display.flip() #updates the visuals on the screen
    pygame.display.update()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            x = playership.movement(x) #GETS NEW X VALUE
            playership.player_action(x,y) #reads what button you press
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

pygame.quit()
