import pygame
from assets import *
from utils import *


class Player(pygame.sprite.Sprite):
    # Constants for player stat types:
    CURRENT_LEVEL_ID = 0
    FULL_HEALTH = 1
    CURRENT_HEALTH = 2
    RUN_SPEED = 3  # Tiles per second
    MELEE_DAMAGE = 4
    MELEE_COOLDOWN_MULTIPLIER = 5
    MAGIC_DAMAGE = 6
    MAGIC_COOLDOWN_MULTIPLIER = 7
    KILLS = 8

    # Minimum and maximum values for starting player stats:
    MIN_HEALTH = 75
    MAX_HEALTH = 125
    MIN_SPEED = 3
    MAX_SPEED = 6
    MIN_MAGIC = 75
    MAX_MAGIC = 125
    MIN_ATTACK = 75
    MAX_ATTACK = 125

    def __init__(self, game, level, position, stats, inventory):

        self.game = game
        self.level = level

        super().__init__()

        # Player stats and inventory dictionaries:
        self.stats = stats
        self.inventory = inventory

        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        tile_size = self.level.get_tile_size()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(center=position)

        # Pygame provides vectors in 2D and 3D, and allows operations to be made using them:
        self.direction = pygame.math.Vector2()

        # For very high frame rates, the number of pixels the player should travel per frame is less than 1.
        # For this reason, storing this value and adding it to the distance each frame:
        self.displacement_deficit = [0, 0]

        self.attacking = False
        self.attack_start_time = 0

        # The collider will allow for the desired overlap effect:
        self.collider = self.rect  # .inflate(0, game.unit_to_pixel(0.001))

    def get_rect(self):
        return self.rect

    def get_stats(self):
        return self.stats

    def handle_input(self):
        # Getting the keys that are being held down:
        keys_held = pygame.key.get_pressed()

        # Calculating the correct direction according to the keys held:
        if keys_held[pygame.K_a] and not keys_held[pygame.K_d]:
            self.direction.x = -1
        elif keys_held[pygame.K_d] and not keys_held[pygame.K_a]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys_held[pygame.K_w] and not keys_held[pygame.K_s]:
            self.direction.y = -1
        elif keys_held[pygame.K_s] and not keys_held[pygame.K_w]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # Normalising the direction vector such that the speed of motion
        # is constant even if the player is moving diagonally:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Attack input:
        if keys_held[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_start_time = pygame.time.get_ticks()
            print("ATTACK")

        if keys_held[pygame.K_LSHIFT] and not self.attacking:
            self.attacking = True
            self.attack_start_time = pygame.time.get_ticks()
            print("MAGIC")

    def update_cooldown_timers(self):
        # The timers for when an action requires a cooldown.
        # Measuring the difference in ticks to calculate time.
        # Alternatively, it is possible to do it by counting frames and multiplying by frame time:

        current_time = pygame.time.get_ticks()

        if current_time - self.attack_start_time >= self.stats[self.MELEE_DAMAGE]:
            self.attacking = False

    def move_player(self, speed):
        # In this implementation, the player is moved as usual, and if there is a collision, the player is moved to the
        # appropriate side of the obstacle, which is determined using the player's direction of motion:

        # For high frame rates, the number of pixels the player moves per frame could be less than 1 pixel per frame.
        # For this reason, storing the distance that the player should have travelled, and moving the player by that
        # distance when it reaches 1:

        speed_per_frame = speed * self.level.get_tile_size() * self.game.get_current_frame_time()

        # How much the player needs to move this frame,
        # taking into account how much it couldn't move in the previous frames:
        displacement_required = [speed_per_frame * axis + self.displacement_deficit[index] for index, axis in
                                 enumerate(self.direction)]

        # How much motion is possible.
        # The number of pixels moved per frame must be an integer,
        # and this can be less than 1 if the frame rate is high:
        displacement_possible = [int(axis) for axis in displacement_required]

        self.displacement_deficit = [displacement_required[0] - displacement_possible[0],
                                     displacement_required[1] - displacement_possible[1]]

        self.collider.x += displacement_possible[0]
        self.handle_collision(0)

        self.collider.y += displacement_possible[1]
        self.handle_collision(1)

        # Centering the rectangle of the player to where the collider has just been moved:
        self.rect.center = self.collider.center

    def handle_collision(self, axis):
        # Retrieving the collision objects:
        obstacle_sprites = self.level.get_obstacle_tiles_in_frame()

        # x-axis:
        if axis == 0:
            for obstacle in obstacle_sprites:
                obstacle_collider = obstacle.get_collider()
                # Checking if the obstacle has collided with the player:
                if obstacle_collider.colliderect(self.collider):
                    # Using the player's direction to stop collision:
                    if self.direction.x > 0:
                        # The player is moving right, move the player to the left of the obstacle:
                        self.collider.right = obstacle_collider.left
                    else:
                        # The player is moving left, move the player to the right of the obstacle:
                        self.collider.left = obstacle_collider.right
        # y-axis:
        else:
            for obstacle in obstacle_sprites:
                obstacle_collider = obstacle.get_collider()
                # Checking if the obstacle has collided with the player:
                if obstacle_collider.colliderect(self.collider):
                    # Using the player's direction to stop collision:
                    if self.direction.y > 0:
                        # The player is moving down, move the player above of the obstacle:
                        self.collider.bottom = obstacle_collider.top
                    else:
                        # The player is moving up, move the player below the obstacle:
                        self.collider.top = obstacle_collider.bottom

    def draw(self, draw_offset):
        pygame.display.get_surface().blit(self.image, self.rect.topleft + draw_offset)

    def get_collider(self):
        return self.collider

    def update(self):
        self.handle_input()
        self.update_cooldown_timers()
        self.move_player(self.stats[self.RUN_SPEED])
