import pygame
import random
import math

# Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

pygame.init()

# Blank Screen:
size = (640,480)
screen = pygame.display.set_mode(size)

# The title of the new window:
pygame.display.set_caption("Snow")

# Defines a class which is a sprite.
class Snow(pygame.sprite.Sprite):
 
    # Define the constructor for snow
    def __init__(self, color, width, height, speed):

        # Calls the sprite constructor.
        super().__init__()

        self.speed = speed

        # Creates a sprite and fills it with 'color'.
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        # Sets the position of the sprite within the range.
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 600)
        self.rect.y = random.randrange(0, 400)

    # Class update function 
    def update(self):
        if self.rect.y + 5 <= 480:
            self.rect.y = self.rect.y + self.speed
        else:
            self.rect.y = 0

                                                                             
def detached(mySnow, snowGroup): # Checks if the new snowflake is detached from all previously creted ones.
    for snow in snowGroup:
        # If for all of the snowflakes, the difference in x or y coordinates is 5 or less, it is not detached. Used 20 to make them spread apart.
        if (abs(mySnow.rect.x - snow.rect.x) < 20) and (abs(mySnow.rect.y - snow.rect.y) < 20):
            return False

    return True


# When this is true, the game will end:
done = False

snowGroup = pygame.sprite.Group() # A list of snow blocks.
allSpritesGroup = pygame.sprite.Group() # A list of all sprites.

numberOfFlakes = 50 # There will be 50 snowflakes.

for x in range(numberOfFlakes):
    isDetached = False
    while not isDetached: #Repeats until the snowflake generated is detached from all others.
        mySnow = Snow(WHITE, 5, 5,1) # The snowflakes are white, 5px squares with a speed if 1px/frame.

        if detached(mySnow, snowGroup):
            snowGroup.add(mySnow) # Adds the new snowflake to the group of snowflakes.
            allSpritesGroup.add(mySnow) # Adds the new snowflake to the group of all sprites.
            isDetached = True   
  
clock = pygame.time.Clock()

### This is the Game Loop:
while not done:

    # User inputs and controls:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #endif
    #Next

    ##The Game Logic:
    allSpritesGroup.update()

    #The screen background is BLACK:
    screen.fill(BLACK)
    
    allSpritesGroup.draw(screen)



    #This will flip the display to reveal the new position of objects:
    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)

#endwhile - The end of the game loop.

pygame.quit()