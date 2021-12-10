import pygame
from pygame import surface

#Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

pygame.init()

map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

mapXSize = len(map[0])
mapYSize = len(map)

# The number of pixels that make up a tile.
pixelPerTile = 40

# The size of the screen should be number of tiles * number of pixels per tile.
size = (mapXSize * pixelPerTile, mapYSize * pixelPerTile)
screen = pygame.display.set_mode(size)

# Sprite Groups:
allSpritesGroup = pygame.sprite.Group()
wallGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()






screenXSize = size[0]
screenYSize = size[1]



class Tile(pygame.sprite.Sprite):

    def __init__(self, color, width, height, xPos, yPos):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos


class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height, xPos, yPos):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)


        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos

    def getPlayerInput(self):
        # Passes the axis and direction of the movement depending on the key pressed.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movePlayer("x", -1)
                if event.key == pygame.K_d:
                    self.movePlayer("x", 1)
                if event.key == pygame.K_w:
                    self.movePlayer("y", -1)
                if event.key == pygame.K_s:
                    self.movePlayer("y", 1)
    
    def movePlayer(self, axis, vector):
        # Moves the player 1 tile in the given direction.
        if axis == "x":
            self.rect.x += vector * pixelPerTile
        elif axis == "y":
            self.rect.y += vector * pixelPerTile

            # TODO: Do not change the movement until collisions are done. After that, make the movement work as intended.
    
    def update(self):
        self.getPlayerInput()



for x in range(mapXSize):
        for y in range(mapYSize):
            if map[x][y] == 1:
                # Assuming the screen is landscape, the following will cause the square map to fill the height of the screen and be centered on the width.
                myWall = Tile(BLUE, (screenYSize / mapXSize), (size[1] / mapYSize), (x * screenYSize / mapXSize) + ((screenXSize - screenYSize) / 2), (y * screenYSize / mapYSize))
                wallGroup.add(myWall)
                allSpritesGroup.add(myWall)

# Creates the player that is 1-tile sized, at the top left corner:
myPlayer = Player(YELLOW, pixelPerTile, pixelPerTile, pixelPerTile, pixelPerTile)
playerGroup.add(myPlayer)
allSpritesGroup.add(myPlayer)

#The title of the new window:
pygame.display.set_caption("PacMan")

#When this is true, the game will end:
done = False

clock = pygame.time.Clock()

while not done:

    screen.fill(BLACK)

    playerGroup.update()
    allSpritesGroup.draw(screen)


    pygame.display.flip()
    clock.tick(60)


pygame.quit()

        
