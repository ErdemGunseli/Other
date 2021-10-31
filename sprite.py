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

# The following hold the x and y positions of the snowflakes.
snowflakeXPositions = []
snowflakeYPositions = []


# The title of the new window:
pygame.display.set_caption("Snow")

# Defines a class which is a sprite.
class snow(pygame.sprite.Sprite):
 
 # Define the constructor for snow
 def __init__(self, color, width, height):

     # Calls the sprite constructor.
    super().__init__()

    # Creates a sprite and fills it with 'color'.
    self.image = pygame.Surface([width,height])
    self.image.fill(color)

    # Sets the position of the sprite within the range.
    self.rect = self.image.get_rect()
    detachedFromAll = False
  
    # Ensure that none of the snowflakes overlap.
    while detachedFromAll == False:
        self.rect.x = random.randrange(0, 600)
        self.rect.y = random.randrange(0, 400)

        detachedFromAll = True
        # If it is the first snowflake, it can go anywhere.
        if len(snowflakeXPositions) != 0: 

            # Goes through the x and y positions of all of the previous snowflakes.
            for i in snowflakeXPositions: 
                for j in snowflakeYPositions:
                    if (self.rect.x + 10 > i and self.rect.x < i) or (self.rect.y + 10 > j and self.rect.y < j):
                        detachedFromAll = False 
                    # If there was a snowflake within 10 px of the current snowflake, the new snowflake cannot go there.
     
    # Adds the x and y positions of the snowflakes to lists to ensure that new snowflakes don't overlap with the old ones.
    snowflakeXPositions.append(self.rect.x)
    snowflakeYPositions.append(self.rect.y)


        

# When this is true, the game will end:
done = False

snowGroup = pygame.sprite.Group() # A list of snow blocks.
allSpritesGroup = pygame.sprite.Group() # A list of all sprites.

numberOfFlakes = 50 # There will be 50 snowflakes.

for x in range(numberOfFlakes):
    mySnow = snow(WHITE, 5, 5) # The snowflakes are white, 5px squares.
    snowGroup.add(mySnow) # Adds the new snowflake to the group of snowflakes.
    allSpritesGroup.add(mySnow) # Adds the new snowflake to the group of all sprites.

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

    #The screen background is BLACK:
    screen.fill(BLACK)
    
    allSpritesGroup.draw(screen)



    

    #This will flip the display to reveal the new position of objects:
    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)

#endwhile - The end of the game loop.

pygame.quit()

        
