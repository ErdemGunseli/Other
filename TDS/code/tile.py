import pygame
from utils import *


# TODO: PASS OBJECT SIZE IN TILES

class Tile(pygame.sprite.Sprite):

    # The size attribute is the size of the tile relative to the default tile size.
    # The collider ratio is what ratio of the size of the object the collider should be.
    # For example, because the player should pass through the leaves of a tree,
    # the collider of the tree should be less than the size of its image, which includes its leaves.
    # If a value in the collider ratio is 0, it will be 1 pixel.
    def __init__(self, position, size=(1, 1), collider_ratio=(0.9, 0.9),
                 surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):

        super().__init__()

        # Setting the correct size for the tile:
        self.image = pygame.transform.scale(surface, [dimension * TILE_SIZE for dimension in size])

        self.rect = self.image.get_rect(bottomleft=position)

        # If any value of the collider ratio is less than or equal to 0, make it 1 pixel:
        collider_ratio = list(collider_ratio)
        for index, value in enumerate(collider_ratio):
           # if value <= 0: collider_ratio[index] = 1 / (size[index] * TILE_SIZE)
            pass

        # TODO: FIX COLLIDER RATIO PROBLEM
        # Adjusting collider according to requirement:
        self.collider = self.rect.inflate([-0.5 * dimension * size[index] * (1 - collider_ratio[index])
                                           for index, dimension in enumerate(self.rect.size)])





