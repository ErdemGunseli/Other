import pygame
import random
import math

from pygame.display import set_palette, update
from pygame.sprite import spritecollide

# Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

pygame.init()

# Blank Screen:
size = (640,480)
screen = pygame.display.set_mode(size)
bullets = 100

invaderGroup = pygame.sprite.Group() # A list of enemies.
allSpritesGroup = pygame.sprite.Group() # A list of all sprites.

numberOfEnemies = 50 # There will be 50 enemies.

playerMovePerFrame = 5 # The number of px the player will move per frame.

# The title of the new window:
pygame.display.set_caption("Invaders")

# Defines a class which is a sprite.
class Invaders(pygame.sprite.Sprite):
 

    def __init__(self, color, width, height, speed): # Constructor

        super().__init__() #Inherits from Sprite Class

        self.speed = speed

        # Creates a sprite and fills it with 'color'.
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        # Sets the position of the sprite within the range.
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 600)
        self.rect.y = random.randrange(-50, 0) 

    # Class update function 
    def update(self):
        if self.rect.y + 5 <= 480:
            self.rect.y = self.rect.y + self.speed
        else:
            self.rect.y = 0


class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height): # Constructor

        super().__init__() # Inherits from Sprite Class

        self.speed = 0  # The speed of the player is 0.

        # Creates a sprite and fills it with 'color'.
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        # Sets the starting location of the player.
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y =  470 

        

    def setPlayerSpeed(self, speed):
        #TODO: Add selection to ensure that the player doesn't go offscreen.
        
            self.speed = speed
            

        
    def update(self):
        self.rect.x += self.speed

def detached(myEnemy, enemyGroup): # Checks if the new enemy is detached from all previously creted ones.
    for enemy in enemyGroup:
        # If for all of the enemies, the difference in x or y coordinates is 10 or less, it is not detached. Used 20 to make them spread apart.
        if (abs(myEnemy.rect.x - enemy.rect.x) < 20) and (abs(myEnemy.rect.y - enemy.rect.y) < 20):
            return False

    return True

# When this is true, the game will end:
done = False

for x in range(numberOfEnemies):
    isDetached = False
    while not isDetached: #Repeats until the enemy generated is detached from all others.
        myInvader = Invaders(BLUE, 10, 10,1) # The enemiws are blue, 10px squares with a speed if 1px/frame.

        if detached(myInvader, invaderGroup):
            invaderGroup.add(myInvader) # Adds the new enemy to the group of enemy.
            allSpritesGroup.add(myInvader) # Adds the new snowflake to the group of all sprites.
            isDetached = True  
 
myPlayer = Player(YELLOW, 10, 10) # The player is a 10px square.
allSpritesGroup.add(myPlayer)
clock = pygame.time.Clock()

### This is the Game Loop:
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                myPlayer.setPlayerSpeed(-5)
            elif event.key == pygame.K_RIGHT:
                myPlayer.setPlayerSpeed(5)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                myPlayer.setPlayerSpeed(0)
    
    ##The Game Logic:
    allSpritesGroup.update()
  
    ##TODO: When an invader hits the player, add 5 to the score.

    # Checks if any invader has collided with the player and removes that invader from the invader group.
    hitPlayerGroup = pygame.sprite.spritecollide(myPlayer, invaderGroup, True)
    
    #The screen background is BLACK:
    screen.fill(BLACK)
    
    allSpritesGroup.draw(screen)
   



    #This will flip the display to reveal the new position of objects:
    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)

#endwhile - The end of the game loop.

pygame.quit()