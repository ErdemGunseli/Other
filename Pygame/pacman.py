import pygame
from pygame import surface

#Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

pygame.init()

#Blank Screen:
size = (640,480)
screen = pygame.display.set_mode(size)

allSpritesGroup = pygame.sprite.Group()
wallGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()


map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

mapXLength = len(map[0])
mapYLength = len(map)

screenXLength = size[0]
screenYLength = size[1]



class Tile(pygame.sprite.Sprite):

    def __init__(self, color, width, height, xPos, yPos):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos


        self.speed = 0
        self.xSpeed = self.speed
        self.ySpeed = self.speed

class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height, xPos, yPos):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)


        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos

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



for x in range(len(map[0])):
        for y in range(len(map)):
            if map[x][y] == 1:
                # Assuming the screen is landscape, the following will cause the square map to fill the height of the screen and be centered on the width.
                myWall = Tile(BLUE, (screenYLength / mapXLength), (size[1] / mapYLength), (x * screenYLength / mapXLength) + ((screenXLength - screenYLength) / 2), (y * screenYLength / mapYLength))
                wallGroup.add(myWall)
                allSpritesGroup.add(myWall)

# Creates the player that is 1-tile sized
myPlayer = Player(YELLOW, (screenYLength / 10),(screenYLength / 10), 200, 200,)
playerGroup.add(myPlayer)
allSpritesGroup.add(myPlayer)



#The title of the new window:
pygame.display.set_caption("My Window")

#When this is true, the game will end:
done = False

clock = pygame.time.Clock()

### This is the Game Loop:

while not done:

    #User inputs and controls:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #endif
    #Next

    ##The Game Logic:

    #The screen background is BLACK:
    screen.fill(BLACK)
        
    

    allSpritesGroup.update()
    allSpritesGroup.draw(screen)

    #This will flip the display to reveal the new position of objects:
    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)

#endwhile - The end of the game loop.

pygame.quit()

        
