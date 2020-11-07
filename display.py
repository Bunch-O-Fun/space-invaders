
import pygame
import sys
import math
import time

SCREEN_HEIGHT = 981                 
SCREEN_WIDTH = 1290 
RIGHT_BORDER = SCREEN_WIDTH - 85        # Border is the maximum a player and alien can go
LEFT_BORDER = 85                        # left or right on the screen

ALIEN_SPEED = 10                        # Number of pixels moved per frame
BULLET_SPEED = 10
PLAYER_SPEED = 5 

class Display:

    
    def __init__ (self):
        '''
        Display Constructor
        Parameters: N/A
        Returns: N/A
        Preconditions: N/A
        Postconditions: creates a valid screen
        '''
        pygame.init()
        global screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        global background
        background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invaders!")
        screen.blit(background,(0,0))


    
    def gameOver(self):
        '''
        Parameters: N/A
        Returns: N/A
        Preconditions: Aliens must have reached a certain threshold on the screen for this to be called
        Postconditions: Displays "Game Over" on screen
        '''
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (400, 250))



class Player:

    
    def __init__(self,xpos,ypos):
        '''
        Player Constructor
        Parameters: xpos, ypos (x and y starting position of player)
        Returns: N/A
        Preconditions: N/A
        Postconditions: creates a valid player at xpos and ypos
        '''
        self.x = xpos
        self.y = ypos
    
        self.direction = 0      #Direction player moves, 1 = right, -1 = left, 0 is dont move
        self.hitbox = pygame.Rect(self.x,self.y,30,30)
        #current player is a square, add graphics later on
    
    
    def move(self):
        '''
        move
        Parameters: N/A
        Returns: N/A
        Preconditions: N/A
        Postconditions: moves player an amount of pixels in a direction 
        '''
        # if statement checks if the player is going outside the border
        if (self.x + self.direction * PLAYER_SPEED > LEFT_BORDER) and (self.x + self.direction * PLAYER_SPEED < RIGHT_BORDER):
            self.x = self.x + self.direction * PLAYER_SPEED

    
    def render(self):
        '''
        render
        Parameters: N/A
        Returns: N/A
        Preconditions: N/A
        Postconditions: renders a 30 x 30 box to represent the player
        '''
        # renders players box and saves it's hit box
        self.hitbox = pygame.Rect(self.x,self.y,30,30)
        pygame.draw.rect(screen,(54,223,42),self.hitbox,0)

class Alien:

    
    def __init__(self,xpos,ypos, xsize, ysize):
        '''
        alien constructor
        Parameters: x and y position, as well as the size in pixels of the alien
        Returns: N/A
        Preconditions: N/A
        Postconditions: creates an alien
        '''
        self.x = xpos
        self.y = ypos
        self.yold = ypos
        self.direction = 1 # 1 = right, -1 = left, 2 & -2 = down
        self.xsize = xsize
        self.ysize = ysize
        self.hitbox = pygame.Rect(self.x,self.y,self.xsize,self.ysize)
        #current player is a square, add graphics later on
    
    
    def move(self):
        '''
        move
        Parameters: N/A
        Returns: N/A
        Preconditions: N/A
        Postconditions: moves an alien in a direction
        '''
        if(abs(self.direction) != 2):
            self.x = self.x + self.direction * ALIEN_SPEED
        else:
            self.y += ALIEN_SPEED


    
    def render(self):
        '''
        render
        Parameters: N/A
        Returns: N/A
        Preconditions: N/A
        Postconditions: updates hitbox and draws self on screen
        '''
        self.hitbox = pygame.Rect(self.x,self.y,self.xsize,self.ysize)
        pygame.draw.rect(screen,(54,223,42),self.hitbox,0)

class Bullet:
    
    def __init__(self, x, y): # initializer for the bullet, allowing specification of its starting location and its speed
        '''
        bullet constructor
        Parameters: x and y position
        Returns: N/A
        Preconditions: N/A
        Postconditions: bullet created at location
        '''
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x,self.y,5,10)

    
    def move(self):
        '''
        move 
        Parameters: N/A
        Returns: N/A
        Preconditions: N/A
        Postconditions: bullet moved upwards
        '''
        self.y -= BULLET_SPEED

    
    def render(self): # this works :)
        '''
        render
        Parameters: N/A
        Returns: N/A
        Preconditions: N/A
        Postconditions: updates hitbox and draws self on screen
        '''
        self.hitbox = pygame.Rect(self.x,self.y,5,10)
        pygame.draw.rect(screen,(255,0,0),self.hitbox,0)



def moveBullets(bullets):
    '''
    move list of bullets
    Parameters: list of bullets you want to move
    Returns: N/A
    Preconditions: N/A
    Postconditions: if bullet exits screen, removes that bullet from the list
    '''
    for bullet in bullets:
        bullet.move()

    if len(bullets) > 0:
        if bullets[0].y < -10:
            bullets.remove(bullets[0])


def moveAliens(aliens):
    '''
    move list of aliens
    Parameters: list of aliens you want to move
    Returns: N/A
    Preconditions: N/A
    Postconditions: if aliens exit screen, ends game
    '''
    # checks if the aliens hit a border, if they do turns them around to go the other way (the aliens move down a bit and then change direction)
    if(len(aliens) != 0):
        if(aliens[len(aliens) - 1].x >= RIGHT_BORDER and aliens[len(aliens) - 1].direction == 1):
            for alien in aliens:
                alien.direction = 2
        elif(aliens[0].x <= LEFT_BORDER and aliens[0].direction == -1):
            for alien in aliens:
                alien.direction = -2
        elif(aliens[0].direction == 2):
            if(aliens[0].y > aliens[0].yold + 40):
                for alien in aliens:
                    alien.direction = -1
                    alien.yold = alien.y
        elif(aliens[0].direction == -2):
            if(aliens[0].y > aliens[0].yold + 40):
                for alien in aliens:
                    alien.direction = 1
                    alien.yold = alien.y

    # moves all the aliens and checks if they leave screen
    for alien in aliens:
        alien.move()
        if(alien.y > SCREEN_HEIGHT):
            running = False


def getUserInput(playership, bullets):
    '''
    gets keypresses like arrow keys and spacebar
    Parameters: playership and list of the player's bullets
    Returns: N/A
    Preconditions: N/A
    Postconditions: user input is updated and executed
    '''
    for event in pygame.event.get():

        # on key pressed, change player direction to arrow key direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playership.direction = -1
            if event.key == pygame.K_RIGHT:
                playership.direction = 1

            # create a bullet if player presses space
            if event.key == pygame.K_SPACE:
                bullets += [Bullet(playership.x + 12, playership.y)]
        
        # on key released change player direction to stop moving
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playership.direction = 0
            if event.key == pygame.K_RIGHT:
                playership.direction = 0
            
            
                        
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()


def checkHit(bullets, aliens):
    '''
    checks if bullet overlaps with alien
    Parameters: list of bullets and aliens
    Returns: N/A
    Preconditions: N/A
    Postconditions: if a alien and bullet overlap deletes them
    '''
    for alien in aliens:
        for bullet in bullets:
            if(alien.hitbox.colliderect(bullet.hitbox)):
                aliens.remove(alien)
                bullets.remove(bullet)


def levelUP(): #Goes to next level if player kills all aliens on current level
    '''
    increments difficulty if all aliens are killed
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: if all aliens dead makes difficulty harder
    '''
    global level, ALIEN_SPEED
    next_level = True
    for row_aliens in aliens:
        if len(row_aliens) != 0:
            next_level = False
    
    if(next_level):
        level += 1
        if(level % 3 == 0):
            ALIEN_SPEED += 2
        for i in range(level % 3 + 1):
            for j in range(15):
                aliens[i] += [Alien(100 + j * 60, 40 + 40 * i, 35, 20)]
    return level


def checkEnd(aliens):
    '''
    checks end condition of game (aliens leave the board)
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: if end condition exits game
    '''
    global running
    for row_aliens in aliens:
        for alien in row_aliens:
            if(alien.y > SCREEN_HEIGHT):
                running = False


def gameLogic(playership, bullets, aliens):
    '''
    executes 1 frame of game logic
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: game is updated to next frame
    '''
    getUserInput(playership, bullets)
    playership.move() #moves player in direction, self.direction updated in playerInput
    moveBullets(bullets)
    moveAliens(aliens[0])
    moveAliens(aliens[1])
    moveAliens(aliens[2])
    checkHit(bullets, aliens[0])
    checkHit(bullets, aliens[1])
    checkHit(bullets, aliens[2])
    levelUP()
    checkEnd(aliens)
    

def render(playership, bullets, aliens):
    '''
    renders 1 frame
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: fram is rendered and ready to flip
    '''
    screen.blit(background,(0,0))
    playership.render()
    for bullet in bullets:
        bullet.render()
    for alien_row in aliens:
        for alien in alien_row:
            alien.render()
    #updates the visuals on the screen
    #pygame.display.update()

if __name__ == '__main__':
    mygame = Display()
    x = 640
    y = 890
    playership = Player(x,y)
    bullets = []
    aliens = [[],[],[]]
    level = 0 
    for i in range(15):
        aliens[0] += [Alien(100 + i * 60, 40, 35, 20)]
    running = True
    while running:
        time_start = pygame.time.get_ticks()
    
        render(playership, bullets, aliens)
        gameLogic(playership, bullets, aliens)
        
        time_end = pygame.time.get_ticks()
        if(time_end - time_start < 17): # regulates framerate to 60fps
            pygame.time.delay(17 - (time_end - time_start))
        pygame.display.flip()
    
    exit_game = False
    mygame.gameOver()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False #breaks out of loop and quits the game
                sys.exit()
