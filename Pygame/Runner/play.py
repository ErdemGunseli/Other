import pygame
from Utils import Utils

pygame.init()
done = False
clock = pygame.time.Clock()
resolution = [1280, 720]
frame_rate = 60
frame_time = 1 / frame_rate

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption(Utils.STRINGS.get("name"))

score = 0

game_font = pygame.font.Font(None, 50)
score_surface = game_font.render(Utils.STRINGS.get("score").format(score), True, Utils.COLORS.get("WHEAT_1"))

background_surface = pygame.image.load(Utils.ASSETS.get("background_layer_1"))
ground_surface = pygame.image.load(Utils.ASSETS.get("dirt_ground"))
snail_surface = pygame.image.load(Utils.ASSETS.get("snail"))
player_surface = pygame.image.load(Utils.ASSETS.get("player_stand"))

background_surface = pygame.transform.scale(background_surface, resolution)
ground_surface = pygame.transform.scale(ground_surface, [resolution[0], resolution[1] * 0.2])
snail_surface = pygame.transform.scale(snail_surface, [75, 75])

background_rect = background_surface.get_rect(topleft=(0, 0))
ground_rect = ground_surface.get_rect(topleft=(0, resolution[1] * 0.8))
score_rect = score_surface.get_rect(topleft=(resolution[0] - 175, 25))
snail_rect = snail_surface.get_rect(topleft=(resolution[0] - 80, resolution[1] * 0.8 - 65))
player_rect = player_surface.get_rect(topleft=(0, resolution[1] * 0.8 - 50))


def update():

   # Snail:
    snail_rect.x -= 100 * frame_time
    if snail_rect.x < -snail_rect.width: snail_rect.x = 0

while not done:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    update()

    screen.blit(background_surface, background_rect)
    screen.blit(ground_surface, ground_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(player_surface, player_rect)
    screen.blit(snail_surface, snail_rect)

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
