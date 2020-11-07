import pygame
import sys
import math
import pygame.mixer
import time
import csv
import pandas as pd

SCREEN_HEIGHT = 981
SCREEN_WIDTH = 1290
RIGHT_BORDER = SCREEN_WIDTH - 85        # Border is the maximum a player and alien can go
LEFT_BORDER = 85                        # left or right on the screen

ALIEN_SPEED = 10                        # Number of pixels moved per frame
BULLET_SPEED = 10
PLAYER_SPEED = 5

df_hs = pd.read_csv("highscores.csv")
print(df_hs)


class Display:

    '''
    Display Constructor
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: creates a valid screen
    '''
    def __init__ (self):
        pygame.init()
        global screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        global background
        background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invaders!")
        screen.blit(background,(0,0))


    '''
    Parameters: N/A
    Returns: N/A
    Preconditions: Aliens must have reached a certain threshold on the screen for this to be called
    Postconditions: Displays "Game Over" on screen
    '''
    def gameOver(self):
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (400, 250))

class Player:

    '''
    Player Constructor
    Parameters: xpos, ypos (x and y starting position of player)
    Returns: N/A
    Preconditions: N/A
    Postconditions: creates a valid player at xpos and ypos
    '''
    def __init__(self,xpos,ypos):
        self.x = xpos
        self.y = ypos

        self.direction = 0      #Direction player moves, 1 = right, -1 = left, 0 is dont move
        self.hitbox = pygame.Rect(self.x,self.y,30,30)
        #current player is a square, add graphics later on

    '''
    move
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: moves player an amount of pixels in a direction
    '''
    def move(self):
        # if statement checks if the player is going outside the border
        if (self.x + self.direction * PLAYER_SPEED > LEFT_BORDER) and (self.x + self.direction * PLAYER_SPEED < RIGHT_BORDER):
            self.x = self.x + self.direction * PLAYER_SPEED

    '''
    render
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: renders a 30 x 30 box to represent the player
    '''
    def render(self):
        # renders players box and saves it's hit box
        self.hitbox = pygame.Rect(self.x,self.y,30,30)
        playerImg = pygame.image.load('player.png')
        screen.blit(playerImg, (self.x,self.y))


class Alien:

    '''
    alien constructor
    Parameters: x and y position, as well as the size in pixels of the alien
    Returns: N/A
    Preconditions: N/A
    Postconditions: creates an alien
    '''
    def __init__(self,xpos,ypos):
        self.x = xpos
        self.y = ypos
        self.yold = ypos
        self.direction = 1 # 1 = right, -1 = left, 2 & -2 = down
        self.xsize = 51
        self.ysize = 51
        self.hitbox = pygame.Rect(self.x,self.y,self.xsize,self.ysize)

    '''
    move
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: moves an alien in a direction
    '''
    def move(self):
        if(abs(self.direction) != 2):
            self.x = self.x + self.direction * ALIEN_SPEED
        else:
            self.y += ALIEN_SPEED


    '''
    render
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: updates hitbox and draws self on screen
    '''
    def render(self):
        self.hitbox = pygame.Rect(self.x,self.y,self.xsize,self.ysize)
        alienImg = pygame.image.load('alien.png')
        screen.blit(alienImg, (self.x,self.y))

class Bullet:
    '''
    bullet constructor
    Parameters: x and y position
    Returns: N/A
    Preconditions: N/A
    Postconditions: bullet created at location
    '''
    def __init__(self, x, y): # initializer for the bullet, allowing specification of its starting location and its speed
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x,self.y,5,10)

    '''
    move
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: bullet moved upwards
    '''
    def move(self):
        self.y -= BULLET_SPEED

    '''
    render
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: updates hitbox and draws self on screen
    '''
    def render(self): # this works :)
        self.hitbox = pygame.Rect(self.x,self.y,5,10)
        pygame.draw.rect(screen,(255,0,0),self.hitbox,0)


'''
move list of bullets
Parameters: list of bullets you want to move
Returns: N/A
Preconditions: N/A
Postconditions: if bullet exits screen, removes that bullet from the list
'''
def moveBullets(bullets):
    for bullet in bullets:
        bullet.move()

    if len(bullets) > 0:
        if bullets[0].y < -10:
            bullets.remove(bullets[0])

'''
move list of aliens
Parameters: list of aliens you want to move
Returns: N/A
Preconditions: N/A
Postconditions: if aliens exit screen, ends game
'''
def moveAliens(aliens):

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

'''
gets keypresses like arrow keys and spacebar
Parameters: playership and list of the player's bullets
Returns: N/A
Preconditions: N/A
Postconditions: user input is updated and executed
'''
def getUserInput(playership, bullets):
    for event in pygame.event.get():

        # on key pressed, change player direction to arrow key direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playership.direction = -1
            if event.key == pygame.K_RIGHT:
                playership.direction = 1

            # create a bullet if player presses space
            if event.key == pygame.K_SPACE:
                #pygame.mixer.music.load('lasershoot.wav')
                #pygame.mixer.music.play(0)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('lasershoot.wav'))
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

'''
checks if bullet overlaps with alien
Parameters: list of bullets and aliens
Returns: N/A
Preconditions: N/A
Postconditions: if a alien and bullet overlap deletes them
'''
def checkHit(bullets, aliens):
    global score
    for alien in aliens:
        for bullet in bullets:
            if(alien.hitbox.colliderect(bullet.hitbox)):
                #pygame.mixer.music.load('invaderkilled.wav')
                #pygame.mixer.music.play(0)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('invaderkilled.wav'))
                aliens.remove(alien)
                bullets.remove(bullet)
                score += 10

'''
increments difficulty if all aliens are killed
Parameters: N/A
Returns: N/A
Preconditions: N/A
Postconditions: if all aliens dead makes difficulty harder
'''
def levelUP(): #Goes to next level if player kills all aliens on current level
    global level, ALIEN_SPEED, level_time_end, level_time_start, score

    next_level = True
    for row_aliens in aliens:
        if len(row_aliens) != 0:
            next_level = False

    if(next_level):
        level_time_end = pygame.time.get_ticks()
        time = (level_time_end - level_time_start) / 1000
        score += 500/(time + 10) + 100
        level += 1
        if(level % 3 == 0):
            ALIEN_SPEED += 2
        for i in range(level % 3 + 1):
            for j in range(15):
                aliens[i] += [Alien(100 + j * 60, 40 + 40 * i, 35, 20)]
        level_time_start = pygame.time.get_ticks()


'''
checks end condition of game (aliens leave the board)
Parameters: N/A
Returns: N/A
Preconditions: N/A
Postconditions: if end condition exits game
'''
def checkEnd(aliens):
    global running
    global score
    for row_aliens in aliens:
        for alien in row_aliens:
            if(alien.y > SCREEN_HEIGHT):
                running = False

'''
executes 1 frame of game logic
Parameters: N/A
Returns: N/A
Preconditions: N/A
Postconditions: game is updated to next frame
'''
def gameLogic(playership, bullets, aliens):
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

'''
renders 1 frame
Parameters: N/A
Returns: N/A
Preconditions: N/A
Postconditions: fram is rendered and ready to flip
'''
def render(playership, bullets, aliens):
    screen.blit(background,(0,0))
    userInterface();
    playership.render()
    for bullet in bullets:
        bullet.render()
    for alien_row in aliens:
        for alien in alien_row:
            alien.render()
     #updates the visuals on the screen
    #pygame.display.update()

def userInterface():
    global score
    global level
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    scoreUI = myfont.render("Score: " + str(score), 1, (255,255,255))
    levelUI = myfont.render("Level: " + str(level), 1, (255,255,255))
    screen.blit(scoreUI, (100, 100))
    screen.blit(levelUI, (100, 50))


mygame = Display()

score = 0

x = 640
y = 890
pygame.mixer.Channel(2).play(pygame.mixer.Sound('backgroundmusic.wav'))
playership = Player(x,y)
bullets = []
aliens = [[],[],[]]
level = 0
for i in range(15):
    aliens[0] += [Alien(100 + i * 60, 40)]
running = True
level_time_start = pygame.time.get_ticks()
level_time_end = 0
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
#df_s = pd.DataFrame([[name, score]], columns = ['Name', 'Score'])
#df_hs = pd.concat([df_s, df_hs])
#df_hs = df_hs.sort_values(by=["Score", "Name"], ascending=False)
#df_hs.to_csv("highscores.csv", index=False)
input_box = pygame.Rect(500, 500, 140, 32)
active = False
text = ''
done = False
font = pygame.font.Font(None,32)
color = pygame.Color('dodgerblue2')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
        color = pygame.Color('lightskyblue3') if active else pygame.Color('dodgerblue2')
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_ESCAPE
            if active:
                if event.key == pygame.K_RETURN:
                    name = text
                    active = False
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            elif event.key == pygame.K_q:
                name = text
                running = False

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface,(input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.display.flip()

df_s = pd.DataFrame([[name, score]], columns = ['Name', 'Score'])
df_hs = pd.concat([df_s, df_hs])
df_hs = df_hs.sort_values(by=["Score", "Name"], ascending=False)
df_hs.to_csv("highscores.csv", index=False)
pygame.quit()
sys.exit()
