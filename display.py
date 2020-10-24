import pygame
import sys
import math
import time

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
        self.x = xpos
        self.y = ypos
        #current player is a square, add graphics later on

    def playerRender(self):
        global playerimg
        playerimg = pygame.Rect(self.x,self.y,30,30)
        pygame.draw.rect(screen,(54,223,42),playerimg,0)

    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Bullet:

    def __init__(self, x, y): # initializer for the bullet, allowing specification of its starting location and its speed
        self.x = x
        self.y = y
        self.printB = False

    def bullet_action(self,x,y):
        self.x = x
        self.y = y
        self.printB = True
        for i in range(455):
            self.y += 1
            self.bulletRender()
            time.sleep(0.025)
            print(self.y)
        self.printB = False

    def bulletRender(self):
        global bulletimg
        bulletimg = pygame.Rect(self.x,self.y,5,10)
        pygame.draw.rect(screen,(54,0,42),bulletimg,0)

def gameLogic(playership, bullet):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if playership.x >= 85:
                    playership.x -= 15
            if event.key == pygame.K_RIGHT:
                if playership.x <= 1195:
                    playership.x += 15
            if event.key == pygame.K_SPACE:
                start_x = playership.getX()
                start_y = playership.getY()
                bullet.bullet_action(start_x,start_y)
        #render(playership, bullet)
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

def render(playership, bullet):
    screen.blit(background,(0,0))
    playership.playerRender()
    #if (bullet.printB == True):
    #bullet.bulletRender()
    pygame.display.flip() #updates the visuals on the screen
    pygame.display.update()

mygame = Display()
x = 640
y = 190
playership = Player(x,y)
bullet = Bullet(playership.x, playership.y)
global running
running = True
while running:
    gameLogic(playership, bullet)
    render(playership, bullet)
    pygame.time.delay(10)
pygame.quit()
