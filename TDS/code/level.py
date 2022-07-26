import pygame.display
from pytmx import *
from utils import *
from tile import Tile
from player import Player
from colours import *
import math
from assets import *


# TODO: Transparent blue rectangle to give night effect

class Level:
    # File names:
    MAP_FILE = "map.tmx"

    # Layer Names:
    GROUND = "ground"
    RIVER = "river"
    ROAD = "road"
    PEBBLES = "pebbles"
    PLANTS = "plants"
    TREES = "trees"
    ROCKS = "rocks"
    BUILDINGS = "buildings"
    BARRIERS = "barriers"
    COLLIDERS = "colliders"

    # Other constants:
    TILE_RESOLUTION = 256
    NIGHT_COLOUR = (0, 71, 171)

    def __init__(self, game, level_id, min_tile_count=15, day_duration=60000):
        self.player = None
        self.game = game
        self.database_helper = game.get_database_helper()

        self.display = pygame.display.get_surface()
        display_size = self.display.get_size()

        # Calculating the pixel size of each tile according to how many should fit on-screen:
        if display_size[0] > display_size[1]:
            self.tile_size = display_size[1] // min_tile_count
        else:
            self.tile_size = display_size[0] // min_tile_count
        # self.tile_size = 10

        self.display_center = (display_size[0] // 2, display_size[1] // 2)

        # Validating level ID:
        if level_id <= 0 or level_id is None:
            self.level_id = 1
        else:
            self.level_id = level_id

        # Draw offset amount such that the player is always centred:
        self.draw_offset = pygame.math.Vector2()

        # Groups determining how the sprites should be categorised.
        # They are not mutually exclusive:
        self.all_tiles = pygame.sprite.Group()  # All the sprites in the level.
        self.flat_tiles = pygame.sprite.Group()   # Sprites with no depth effect.
        self.depth_tiles = pygame.sprite.Group()  # Sprites with depth effect.
        self.obstacle_tiles = pygame.sprite.Group()   # Sprites that have collision.
        self.depth_tiles_in_frame = pygame.sprite.Group() # Depth sprites that are on-screen.
        self.flat_tiles_in_frame = pygame.sprite.Group()   # Flat sprites that are on-screen.
        self.obstacle_tiles_in_frame = pygame.sprite.Group()   # Obstacle sprites that are on-screen.

        # Importing map path:
        level_id = int(level_id)
        if level_id is None or level_id == 0:
            level_id = 1
        self.path = self.database_helper.get_map_path(level_id)

        # Setting the scale factor for the correct conversion of the position of objects:
        self.scale_factor = self.TILE_RESOLUTION / self.tile_size


        # Getting background colour:
        self.background_colour = self.database_helper.get_background_colour(self.level_id)

        self.tmx_data = load_pygame(self.path + "/" + self.MAP_FILE)
        self.set_up_map()


    def set_up_map(self):

        # TODO: GET PLAYER INVENTORY AND STATS
        # TODO: UPDATE CURRENT LEVEL ID ? WILL IT NEED UPDATING? YES
        # TODO: Run speed should be a number of tiles per second

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
        self.depth_tiles.add(self.player)
        self.all_tiles.add(self.player)

        # Setting up layers:
        self.set_up_layer(self.RIVER, visible=True, depth=False, obstacle=False)
        self.set_up_layer(self.ROAD, visible=True, depth=False, obstacle=False)
        self.set_up_layer(self.PEBBLES, collider_ratio=(0.5, 0.5), visible=True, depth=True, obstacle=True)
        self.set_up_layer(self.PLANTS, visible=True, depth=True, obstacle=False)
        self.set_up_layer(self.TREES, collider_ratio=(0.6, 0.4), visible=True, depth=True, obstacle=True)
        self.set_up_layer(self.ROCKS, collider_ratio=(0.7, 0.7), visible=True, depth=True, obstacle=True)
        # Because buildings can have different shapes, their colliders are made of individual barriers:
        self.set_up_layer(self.BUILDINGS, visible=True, depth=True, obstacle=False)
        self.set_up_layer(self.BARRIERS, collider_ratio=(1, 1), visible=True, obstacle=True)
        self.set_up_layer(self.COLLIDERS, collider_ratio=(1, 1), visible=True, obstacle=True)

    def set_up_layer(self, layer_name, collider_ratio=(0.9, 0.9), visible=True, depth=True, obstacle=True):
        # Could not find a way to handle tile rotation or flipping - the pytmx docs say that this is
        # automatically handled when getting the image, but not working for me :/

        # Return if a given layer is not present in this map:
        if layer_name not in [layer.name for layer in self.tmx_data.visible_layers]: return

        layer = self.tmx_data.get_layer_by_name(layer_name)

        # If object layer:
        if isinstance(layer, TiledObjectGroup):
            for map_object in layer:
                if map_object.image is not None:
                    # Adjusting for any rotation:
                    image = pygame.transform.rotate(map_object.image, map_object.rotation)
                    tile = Tile(self, (map_object.x / self.scale_factor, (map_object.y / self.scale_factor) + 1),
                                layer_name,
                                size=(map_object.width / self.TILE_RESOLUTION, map_object.height / self.TILE_RESOLUTION),
                                collider_ratio=collider_ratio, surface=image, protect_aspect_ratio=False)
                    # Adding to correct groups:
                    if visible:
                        if depth:
                            self.depth_tiles.add(tile)
                        else:
                            self.flat_tiles.add(tile)
                    if obstacle:
                        self.obstacle_tiles.add(tile)
                    self.all_tiles.add(tile)

        # If tile layer:
        elif isinstance(layer, TiledTileLayer):
            for x, y, surface in layer.tiles():
                if surface is not None:
                    tile = Tile(self, (x * self.tile_size, y * self.tile_size), layer_name, collider_ratio=collider_ratio,
                                surface=surface, protect_aspect_ratio=True)
                    # Adding to correct groups:
                    if visible:
                        if depth:
                            self.depth_tiles.add(tile)
                        else:
                            self.flat_tiles.add(tile)
                    if obstacle:
                        self.obstacle_tiles.add(tile)
                    self.all_tiles.add(tile)


    def draw_map(self):
        # Calculating how far the player is from the centre of the screen,
        # and determining correct offset such that the player is back at the centre:
        self.draw_offset.x = self.display_center[0] - self.player.get_rect().centerx
        self.draw_offset.y = self.display_center[1] - self.player.get_rect().centery

        # Checking which sprites are on-screen, as we only need to be concerned with those:
        self.update_sprites_in_frame()

        # First drawing sprites without depth effect:
        for tile in self.flat_tiles_in_frame:
            tile.draw(self.draw_offset)

        # Sorting sprites with depth effect in ascending order of y-position:
        for tile in sorted(self.depth_tiles_in_frame, key=lambda sprite_in_list: sprite_in_list.rect.centery):
            tile.draw(self.draw_offset)

    def update_sprites_in_frame(self):
        self.depth_tiles_in_frame = pygame.sprite.Group()
        self.obstacle_tiles_in_frame = pygame.sprite.Group()
        self.flat_tiles_in_frame = pygame.sprite.Group()

        # Calculating the rect of the screen such that we can work out if objects are on screen:
        screen_rect = self.game.get_rect().copy()
        screen_rect.center = self.player.get_rect().center

        for sprite in self.depth_tiles:
            if pygame.Rect.colliderect(sprite.rect, screen_rect):
                self.depth_tiles_in_frame.add(sprite)

        for sprite in self.obstacle_tiles:
            if pygame.Rect.colliderect(sprite.rect, screen_rect):
                self.obstacle_tiles_in_frame.add(sprite)

        for sprite in self.flat_tiles:
            if pygame.Rect.colliderect(sprite.rect, screen_rect):
                self.flat_tiles_in_frame.add(sprite)

    def get_background_colour(self):
        return self.background_colour

    def get_id(self):
        return self.level_id

    def get_obstacle_tiles(self):
        return self.obstacle_tiles

    def get_all_tiles(self):
        return self.all_tiles

    def get_tile_size(self):
        return self.tile_size

    def get_tmx_data(self):
        return self.tmx_data

    def get_tile_size(self):
        return self.tile_size

    def get_scale_factor(self):
        return self.scale_factor

    def update(self):
        self.all_tiles.update()
        self.draw_map()

