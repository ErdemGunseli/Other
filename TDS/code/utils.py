import pygame
from csv import reader
from os import walk


# TODO: SET TILE SIZE DYNAMICALLY SO THAT THERE IS A FIXED AMOUNT OF TILES FIT IN MAP
TILE_SIZE = 64


# Imports a layout file of which there are many per level:
def import_csv_layout(path):
    terrain_map = []

    # Turning the CVS layout file into a list:
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")

        for row in layout:
            terrain_map.append(list(row))

    # Returning a list of tile IDs:
    return terrain_map

# Using this function to import several files at once:
def import_folder(path):
    # Pygame needs to be initiated for this function to work:

    surface_list = []

    for _, __, image_files in walk(path):
        # The data_item variable contains a tuple.
        # 0: path,
        # 1: List of folders in path
        # 2: list of files in our current path

        # The image variable will be a string of the file name:
        for image_file in image_files:
            # The full path to reach the image:
            full_path = path + "/" + image_file

            # Creating a surface using the image retrieved:
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list



