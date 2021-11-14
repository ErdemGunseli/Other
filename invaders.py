
import pygame
import random
import math
from pygame.constants import K_DOWN
from pygame.display import set_palette, update
from pygame.event import pump
from pygame.sprite import spritecollide
from pygame.constants import K_UP
pygame.font.init()

#TODO: Improve movement.
#TODO: Have the while loop minimised.
#TODO: Make multiple levels.
#TODO: Make the enemies disappear when hit and add 5 to the bullet count as well as 1 to the score.

# Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,100, 50)
PURPLE = (200,100,255)

pygame.init()

# Blank Screen:
size = (640,480)
screen = pygame.display.set_mode(size)
bullets = 100

maxInvaderSpeed = 10

invaderGroup = pygame.sprite.Group() # A list of enemies.
bulletGroup = pygame.sprite.Group() # A list of bullets.
allSpritesGroup = pygame.sprite.Group() # A list of all sprites.


invaderCount = 20 # There will be 20 enemies.

playerMovePerFrame = 5 # The number of px the player will move per frame.

defaultFont = pygame.font.SysFont('Comic Sans MS', 15)

# The title of the new window:
pygame.display.set_caption("Invaders")


class GameLogic():

    def __init__(self):
        pass

    def startGame(self, allSpritesGroup):
        allSpritesGroup = []
        self.generateInvaders()
        self.generatePlayer(self)
        return allSpritesGroup

    def endGame(self):
        # Displays end message and awaits input to restart game.
        screen.fill(BLACK)
        defeatDisplay = defaultFont.render("GAME OVER \n  PRESS ESC TO RESTART", False, RED)
        screen.blit(defeatDisplay, (160, 200))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    for i in invaderGroup:
                        i.kill()
                    for j in bulletGroup:
                        j.kill()
                    self.myPlayer.kill()
                    GameLogic.startGame(GameLogic, allSpritesGroup)

    def generateInvaders():
        # Generates the invaders.
        for x in range(invaderCount):
            myInvader = Invaders(PURPLE, 10, 10, 1) # The enemies are blue, 10px squares with a speed if 1px/frame
            invaderGroup.add(myInvader) # Adds the new enemy to the group of enemy.
            allSpritesGroup.add(myInvader) # Adds the new snowflake to the group of all sprites.

    def generatePlayer(self):    
        # Generates the player.
        self.myPlayer = Player(YELLOW, 10, 10, 50) # The player is a 10px square.
        allSpritesGroup.add(self.myPlayer)


    def update(self):
        if self.myPlayer.alive:
            screen.fill(BLACK)

            allSpritesGroup.update()

            allSpritesGroup.draw(screen)
        else:
            self.endGame(self)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

            



# Defines a class which is a sprite.
class Invaders(pygame.sprite.Sprite):
 

    def __init__(self, color, width, height, speed): # Constructor

        super().__init__() #Inherits from Sprite Class

        self.speed = speed
        self.xSpeed = speed * random.randrange(-1, 2)
        self.ySpeed = speed * random.randrange(1, 3)

        # Creates a sprite and fills it with 'color'.
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        # Sets the position of the sprite within the range.
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(30, 600)
        self.rect.y = random.randrange(-500, 0) 

    # Class update function 
    def update(self):
        if self.rect.y > 700:
            self.rect.y = -60
        elif self.rect.x <= 0 or self.rect.x >= 630:
            self.xSpeed = -self.xSpeed

        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
       

class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height, bulletCount): # Constructor

        super().__init__() # Inherits from Sprite Class

        self.speed = 0  # The speed of the player is 0.
        self.xSpeed = self.speed
        self.ySpeed = self.speed
        
        self.lives = 5
        self.bulletCount = bulletCount
        self.score = 0

        self.width = width
        self.height = height

        self.quit = False

        self.alive = True

        # Creates a sprite and fills it with 'color'.
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        # Sets the starting location of the player.
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y =  470 
       
    def bulletShooter(self):
        # Shoots a bullet if there are any.
        if self.bulletCount > 0:
            myBullet = Bullet(self.rect.x + 0.5 * self.width, self.rect.y )
            bulletGroup.add(myBullet)
            allSpritesGroup.add(myBullet)

            self.bulletCount -= 1

    def playerScoreDisplayer(self): # TODO: Move this to the game class.
        # Displays information.
        myLives = defaultFont.render("LIVES:  {}".format(self.lives), False, RED)
        myBulletCount = defaultFont.render("AMMO: {}".format(self.bulletCount), False, RED)
        myScore = defaultFont.render("SCORE: {}".format(self.score), False, RED)
        myInvaderCount = defaultFont.render("INVADERS LEFT:  {}".format(len(invaderGroup)), False, RED)
        
        screen.blit(myLives, (20,0))
        screen.blit(myBulletCount, (20, 20))
        screen.blit(myScore, (20, 40))
        screen.blit(myInvaderCount, (20, 60))
        
    def decreaseLife(self):
        if self.lives > 1:
            self.lives -= 1
        else:
            self.alive = False

    def setScore(self, score):
        # Sets the score of the player.
        self.score = score
        

    def setPlayerSpeed(self, coordinate, speed):
        # Sets the player's speed, the direction of which is determined by the argument passed.
        if coordinate == "x":
            self.xSpeed = speed
        elif coordinate == "y":
            self.ySpeed = speed

    def update(self):

        # Gets the player input.
        self.playerInput()
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed

        # Sets the player's score depending on the number of enemies left and displays it.
        self.setScore((invaderCount - len(invaderGroup)) * 10)
        self.playerScoreDisplayer()

        # Checks if any invader has collided with the player and removes that invader from the invader group.
        hitPlayerGroup = pygame.sprite.spritecollide(self, invaderGroup, True)
    
        # Calls the function that decreases the player's lives.
        for i in hitPlayerGroup:
            self.decreaseLife()


    def playerInput(self):

        # User Inputs:
        # Since the player can move up and down as well, the arguments include which axis to move the player in.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.setPlayerSpeed("x",-5)
                if event.key == pygame.K_d:
                    self.setPlayerSpeed("x",5)
                if event.key == pygame.K_w:
                    self.setPlayerSpeed("y",-5)
                if event.key == pygame.K_s:
                    self.setPlayerSpeed("y",5)
                if event.key == pygame.K_SPACE:
                    self.bulletShooter()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.setPlayerSpeed("x",0)
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self.setPlayerSpeed("y",0)

        # Ensures that the player cannot leave the screen:
        if self.rect.x < 0: self.rect.x = 0
        elif self.rect.x > 630: self.rect.x = 630

        if self.rect.y < 0: self.rect.x = 0
     
        elif self.rect.y > 470: self.rect.y = 470


class Bullet(pygame.sprite.Sprite):
    def __init__(self, xSpawn, ySpawn):
        super().__init__()

        self.speed = 2
        self.color = RED

        self.image = pygame.Surface([2,2])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.rect.x = xSpawn
        self.rect.y = ySpawn

    def update(self):
        self.rect.y -= 2 #Moves up
        
        for i in bulletGroup: # Removes invaders which have been hit by bullets
            pygame.sprite.spritecollide(i, invaderGroup, True)
        



GameLogic.startGame(GameLogic, allSpritesGroup)
done = False

### This is the Game Loop:
while GameLogic.myPlayer.quit == False: 
    

    GameLogic.update(GameLogic)



pygame.quit()