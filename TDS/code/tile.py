import pygame
from utils import *


class Tile(pygame.sprite.Sprite):

    # The size attribute is the size of the tile relative to the default tile size.
    # The collider ratio is what ratio of the size of the object the collider should be.
    # For example, because the player should pass through the leaves of a tree,
    # the collider of the tree should be less than the size of its image, which includes its leaves.
    # If a value in the collider ratio is 0, it will be 1 pixel.
    def __init__(self, level, position, size=(1, 1), collider_ratio=(0.9, 0.9), surface=None, protect_aspect_ratio=True):

        super().__init__()

        tile_size = level.get_tile_size()
        if surface is None:
            surface = pygame.Surface((tile_size, tile_size))

        self.image = surface

        # Resizing the tile whilst protecting the aspect ratio of the source image:
        if protect_aspect_ratio:
            self.resize_image([dimension * tile_size for dimension in size])
        else:
            self.image = pygame.transform.scale(self.image, [dimension * tile_size for dimension in size])


        self.rect = self.image.get_rect(topleft=position)

        # TODO: FIX COLLIDER RATIOOOO
        # TODO: HAVE A WAY TO ALIGN THE COLLIDER TO A SIDE OF THE IMAGE
        # If any value of the collider ratio is less than or equal to 0, make it 1 pixel:
        collider_ratio = list(collider_ratio)
        for index, value in enumerate(collider_ratio):
           # if value <= 0: collider_ratio[index] = 1 / (size[index] * TILE_SIZE)
            pass

        # TODO: FIX COLLIDER RATIO PROBLEM
        # Adjusting collider according to requirement:
        self.collider = self.rect.inflate([-0.5 * dimension * size[index] * (1 - collider_ratio[index])
                                           for index, dimension in enumerate(self.rect.size)])



    def resize_image(self, size):
        current_image_size = self.image.get_size()
        width = current_image_size[0]
        height = current_image_size[1]

        if width > height:
            scale_factor = size[0] / width
            width = size[0]
            height *= scale_factor
        else:
            scale_factor = size[1] / height
            height = size[1]
            width *= scale_factor

        # Setting the icon with the adjusted size:
        self.image = pygame.transform.scale(self.image, (width, height))


    def get_collider(self):
        return self.collider




