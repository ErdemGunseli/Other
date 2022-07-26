import pygame
from utils import *
from colours import *


class Tile(pygame.sprite.Sprite):

    # The size attribute is the size of the tile relative to the default tile size.
    # The collider ratio is what ratio of the size of the object the collider should be.
    # For example, because the player should pass through the leaves of a tree,
    # the collider of the tree should be less than the size of its image, which includes its leaves.
    # If a value in the collider ratio is 0, it will be 1 pixel.
    def __init__(self, level, position, layer_name, size=(1, 1),
                 collider_ratio=(0.9, 0.9), surface=None, protect_aspect_ratio=True):

        super().__init__()

        # The layer name of the tile, which can be used for damage, audio, etc.
        self.layer_name = layer_name

        tile_size = level.get_tile_size()
        if surface is None:
            surface = pygame.Surface((tile_size, tile_size))
        self.image = surface

        if protect_aspect_ratio:
            # Resizing the tile whilst protecting the aspect ratio of the source image:
            self.resize_image([dimension * tile_size for dimension in size])
        else:
            # Resizing the image without protecting the aspect ratio:
            self.image = pygame.transform.scale(self.image, [dimension * tile_size for dimension in size])

        self.rect = self.image.get_rect(topleft=position)


        # The size of the collider should be different to the size of the image for a more realistic result.
        # Adjusting the size of the collider as required:
        self.collider = self.rect.copy().inflate([-(1 - collider_ratio[index]) * dimension
                                                  for index, dimension in enumerate(self.rect.size)])

        # The image of the collider (for debugging, testing etc.):
        self.collider_image = pygame.Surface([self.collider.width, self.collider.height])
        self.collider_image.set_alpha(128)
        self.collider_image.fill(RED)


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

    def draw(self, draw_offset):
        pygame.display.get_surface().blit(self.image, self.rect.topleft + draw_offset)
        pygame.display.get_surface().blit(self.collider_image, self.collider.topleft + draw_offset)

    def get_collider(self):
        return self.collider

    def get_layer_name(self):
        return self.layer_name




