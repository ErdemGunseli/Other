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
        self.all_sprites = pygame.sprite.Group()  # All the sprites in the level.
        self.flat_sprites = pygame.sprite.Group()   # Sprites with no depth effect.
        self.visible_sprites = pygame.sprite.Group()   # Sprites that should be drawn.
        self.obstacle_sprites = pygame.sprite.Group()   # Sprites that have collision.
        self.flat_sprites_in_frame = pygame.sprite.Group()   # Flat sprites that are on-screen.
        self.visible_sprites_in_frame = pygame.sprite.Group()   # Visible sprites that are on-screen.
        self.obstacle_sprites_in_frame = pygame.sprite.Group()   # Obstacle sprites that are on-screen.

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
        self.visible_sprites.add(self.player)
        self.all_sprites.add(self.player)

        # Setting up layers:
        self.set_up_layer(self.RIVER, visible=True, obstacle=False, flat=True)
        self.set_up_layer(self.ROAD, visible=True, obstacle=False, flat=True)
        self.set_up_layer(self.PEBBLES, collider_ratio=(0.5, 0.5), visible=True, obstacle=True, flat=False)
        self.set_up_layer(self.PLANTS, visible=True, obstacle=False)
        self.set_up_layer(self.TREES, collider_ratio=(0.6, 0.4), visible=True, obstacle=True)
        self.set_up_layer(self.ROCKS, collider_ratio=(0.7, 0.7), visible=True, obstacle=True)
        # Because buildings can have different shapes, their colliders are made of individual barriers:
        self.set_up_layer(self.BUILDINGS, visible=True, obstacle=False)
        self.set_up_layer(self.BARRIERS, collider_ratio=(1, 1), visible=True, obstacle=True)
        self.set_up_layer(self.COLLIDERS, collider_ratio=(1, 1), visible=True, obstacle=True)

    def set_up_layer(self, layer_name, collider_ratio=(0.9, 0.9), visible=True, obstacle=True, flat=False):

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
                        if flat:
                            self.flat_sprites.add(tile)
                        else:
                            self.visible_sprites.add(tile)
                    if obstacle:
                        self.obstacle_sprites.add(tile)
                    self.all_sprites.add(tile)

        # If tile layer:
        elif isinstance(layer, TiledTileLayer):
            for x, y, surface in layer.tiles():
                if surface is not None:
                    tile = Tile(self, (x * self.tile_size, y * self.tile_size), layer_name, collider_ratio=collider_ratio,
                                surface=surface, protect_aspect_ratio=True)
                    # Adding to correct groups:
                    if visible:
                        if flat:
                            self.flat_sprites.add(tile)
                        else:
                            self.visible_sprites.add(tile)
                    if obstacle: self.obstacle_sprites.add(tile)
                    self.all_sprites.add(tile)


    def draw_map(self):
        # Calculating how far the player is from the centre of the screen,
        # and determining correct offset such that the player is back at the centre:
        self.draw_offset.x = self.display_center[0] - self.player.get_rect().centerx
        self.draw_offset.y = self.display_center[1] - self.player.get_rect().centery

        # Checking which sprites are on-screen, as we only need to be concerned with those:
        self.update_sprites_in_frame()

        # First drawing sprites without depth effect:
        for sprite in self.flat_sprites_in_frame:
            sprite.draw(self.draw_offset)

        # Sorting sprites with depth effect in ascending order of y-position:
        for sprite in sorted(self.visible_sprites_in_frame, key=lambda sprite_in_list: sprite_in_list.rect.centery):
            sprite.draw(self.draw_offset)

    def update_sprites_in_frame(self):
        self.visible_sprites_in_frame = pygame.sprite.Group()
        self.obstacle_sprites_in_frame = pygame.sprite.Group()
        self.flat_sprites_in_frame = pygame.sprite.Group()

        # Calculating the rect of the screen such that we can work out if objects are on screen:
        screen_rect = self.game.get_rect().copy()
        screen_rect.center = self.player.get_rect().center

        for sprite in self.visible_sprites:
            if pygame.Rect.colliderect(sprite.rect, screen_rect):
                self.visible_sprites_in_frame.add(sprite)

        for sprite in self.obstacle_sprites:
            if pygame.Rect.colliderect(sprite.rect, screen_rect):
                self.obstacle_sprites_in_frame.add(sprite)

        for sprite in self.flat_sprites:
            if pygame.Rect.colliderect(sprite.rect, screen_rect):
                self.flat_sprites_in_frame.add(sprite)

    def calculate_filter_alpha(self):
        current_time = pygame.time.get_ticks()
        current_day_time = current_time % self.day_duration

        result = self.night_filter_max_alpha * math.sin((current_day_time / self.day_duration) * math.pi)
        print(result)
        return int(result)

    def get_current_background_colour(self):
        return self.background_colour

    def get_id(self):
        return self.level_id

    def get_obstacle_sprites(self):
        return self.obstacle_sprites

    def get_tile_size(self):
        return self.tile_size

    def get_tmx_data(self):
        return self.tmx_data

    def get_tile_size(self):
        return self.tile_size

    def get_scale_factor(self):
        return self.scale_factor

    def update(self):
        self.visible_sprites.update()
        self.draw_map()

