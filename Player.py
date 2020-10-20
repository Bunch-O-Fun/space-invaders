from Bullet import Bullet

class Player:

    __position__ = [0,0] # player keeps track of its location via a 2 element array (x,y) 
                         # may be unnecessary as player only moves on one axis (x axis)
    __isAlive__ = True # player keeps track of whether or not it's alive via a boolean

    def __init__(self, x, y): # initializer for the player, allowing specification for starting position and sets life status to True
        self.__position__[0] = x
        self.__position__[1] = y
        self.__isAlive__ = True
    def moveLeft(self): # decrements the player's x coordinate (moves 1 to the left)
        self.__position__[0] = self.__position__[0] - 1
    def moveRight(self): # increments the player's x coordinate (moves 1 to the right)
        self.__position__[0] = self.__position__[0] + 1

    def shoot(self, x, y): # calls an instance of a Bullet
        return Bullet(x+2, y) # (x+2) assuming that __position__ is the upper left corner of the player's ship, and the player's ship is 3x5

    def dead(self): # sets the player's __isAlive__ boolean to false, effectively "killing" the player
        self.__isAlive__ = False
    def getLifeStatus(self): # returns the player's life status
        return self.__isAlive__
    


