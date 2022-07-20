import pygame.display
from pytmx.util_pygame import load_pygame
from utils import *
from tile import Tile
from player import Player


# TODO: Transparent blue rectangle to give night effect

class Level:
    BOUNDARY = 0
    FOLIAGE = 1
    LEVEL_OBJECT = 2

    def __init__(self, game, level_id):
        self.player = None
        self.game = game
        self.database_helper = game.get_database_helper()

        self.display = pygame.display.get_surface()
        self.display_center = (self.display.get_size()[0] // 2, self.display.get_size()[1] // 2)

        self.level_id = level_id

        # Draw offset amount such that the player is always centred:
        self.draw_offset = pygame.math.Vector2()

        # Groups determining how the sprites should be categorised.
        # They are not mutually exclusive:
        self.flat_sprites = pygame.sprite.Group()  # Sprites with no depth effect that should be drawn.
        self.dynamic_sprites = pygame.sprite.Group()  # Sprites that should be updated.
        self.visible_sprites = pygame.sprite.Group()  # Sprites that should be drawn.
        self.obstacle_sprites = pygame.sprite.Group()  # Sprites that have collision.

        # Importing map path:
        level_id = int(level_id)
        if level_id is None or \
                level_id == 0:
            level_id = 1
        self.set_up_map(self.database_helper.get_level_path(level_id))


    def set_up_map(self, path):
        # Loading layout file:
        for layer in load_pygame(path).layers:
            # If statements in outer for loop for improved efficiency at the cost of simplicity:
            tiles = layer.tiles()
            if layer.name == "ground":
                for x, y, surface in tiles:
                    tile = Tile((x * TILE_SIZE, y * TILE_SIZE), surface=surface)
                    self.flat_sprites.add(tile)

            elif layer.name == "mountains":
                for x, y, surface in tiles:
                    tile = Tile((x * TILE_SIZE, y * TILE_SIZE), surface=surface, collider_ratio=(1, 1))
                    self.visible_sprites.add(tile)
                    self.obstacle_sprites.add(tile)
                    print(tile.collider.size)

            else:
                for x, y, surface in tiles:
                    tile = Tile((x * TILE_SIZE, y * TILE_SIZE), surface=surface)
                    self.visible_sprites.add(tile)

                # TODO: GET PLAYER INVENTORY AND STATS
                # TODO: UPDATE CURRENT LEVEL ID ? WILL IT NEED UPDATING?
                # TODO: Run speed should be a number of tiles per second
                # TODO: Set Player Position from special layer in map data, since currently, it depends on tile size

        player_stats = self.database_helper.get_player_stats()


        self.player = Player(self, self.game, (1000, 1000), {Player.CURRENT_LEVEL_ID: self.level_id,
                                                             Player.MAX_HEALTH: 100,
                                                             Player.CURRENT_HEALTH: 100,
                                                             # Run speed is tiles per second
                                                             Player.RUN_SPEED: 5,
                                                             Player.MELEE_DAMAGE: 100,
                                                             Player.RANGED_DAMAGE: 100,
                                                             Player.DAYS_SURVIVED: 100,
                                                             Player.KILLS: 100}, {})
        self.visible_sprites.add(self.player)
        self.dynamic_sprites.add(self.player)

    def calculate_object_size(self, image, small_side=1):
        current_image_size = image.get_size()
        image_width = current_image_size[0]
        image_height = current_image_size[1]

        # Setting the small side to the desired number of tiles
        # whilst protecting the aspect ratio:
        if image_width > image_height:
            scale_factor = small_side / image_height
            image_height = small_side
            image_width *= scale_factor
        else:
            scale_factor = small_side / image_width
            image_width = small_side
            image_height *= scale_factor

        return image_width, image_height

    def draw_visible_sprites(self):
        # Calculating how far the player is from the centre of the screen,
        # and determining correct offset such that the player is back at the centre:
        self.draw_offset.x = self.display_center[0] - self.player.get_rect().centerx
        self.draw_offset.y = self.display_center[1] - self.player.get_rect().centery

        # Drawing sprites without depth effect first:
        for sprite in self.flat_sprites:
            offset_position = sprite.rect.topleft + self.draw_offset
            self.display.blit(sprite.image, offset_position)

        # Sorting sprites in ascending order of y-position:
        for sprite in sorted(self.visible_sprites, key=lambda sprite_in_list: sprite_in_list.rect.midbottom[1]):
            offset_position = sprite.rect.topleft + self.draw_offset
            self.display.blit(sprite.image, offset_position)


    def get_obstacle_sprites(self):
        return self.obstacle_sprites

    def update(self):
        self.dynamic_sprites.update()
        self.draw_visible_sprites()
