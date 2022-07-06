import os

import random
import pygame
import pydoc
import sqlite3
from Colours import *
from Strings import *


class Game:

    random.randint()
    def __init__(self):
        self.done = False
        self.page = 0

        self.database_helper = DatabaseHelper()

        # Default resolution TODO: Make configurable
        self.resolution = (1280, 720)
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(GAME_NAME)

        self.clock = pygame.time.Clock()
        self.frame_rate = 60

        ## Testing TODO: Remove ##
        test_player = Player(None, "Erdem", {})

        generated_id = self.database_helper.save_player(test_player)
        test_player.set_id(generated_id)

        self.database_helper.get_player(generated_id)

        test_player.set_inventory({
            COINS: 150,
            LIVES: 123
        })

        self.database_helper.save_player(test_player)

        test_player.set_inventory({
            COINS: 500,
            LIVES: 500
        })

        self.database_helper.save_player(test_player)

        self.database_helper.get_item_description(COINS)

        #####

        pygame.init()

        self.update()

    def get_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            elif event.type == pygame.KEYDOWN:
                match event.key:

                    case pygame.K_ESCAPE:
                        self.show_main_menu()
                    case pygame.K_o:
                        self.show_settings()
                    case pygame.K_h:
                        self.show_help()
                    case pygame.K_e:
                        self.show_inventory()
                    case pygame.K_m:
                        self.show_map()
                    case _:
                        print("Waiting")

    def update(self):
        while not self.done:
            self.get_input()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

        pygame.quit()

    def show_main_menu(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, RED, (0, 0, 100, 100))

    def show_settings(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, GREEN, (0, 0, 100, 100))

    def show_help(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, BLUE, (0, 0, 100, 100))

    def show_game(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 100, 100))

    def show_inventory(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, YELLOW, (0, 0, 100, 100))

    def show_map(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, CYAN, (0, 0, 100, 100))


class Player:

    def __init__(self, player_id, name, inventory):
        self.id = player_id
        self.name = name
        self.inventory = inventory

    def get_id(self): return self.id

    def set_id(self, player_id): self.id = player_id

    def get_name(self): return self.name

    def set_name(self, name): self.name = name

    def get_inventory(self): return self.inventory

    def set_inventory(self, inventory): self.inventory = inventory


class DatabaseHelper:

    def __init__(self):

        self.DB = "saves.db"

        # Checking that the database does not already exist:
        if os.path.isfile(self.DB): return

        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        # Players table stores the players, the progress of whom are separate:
        cursor.execute("""CREATE TABLE IF NOT EXISTS PLAYERS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT NOT NULL
                        )""")

        # TODO: Add ID field?
        # Items table stores item types and their descriptions:
        cursor.execute("""CREATE TABLE IF NOT EXISTS ITEMS(
                                    NAME TEXT PRIMARY KEY NOT NULL,
                                    DESCRIPTION TEXT NOT NULL
                               )""")

        # Inserting item types that are in the game:
        cursor.executemany("INSERT INTO ITEMS VALUES(?, ?)", [(LIVES, DESC_LIVES), (COINS, DESC_COINS)])

        # Inventory Items table stores every item in the inventory of every player alongside their quantity:
        cursor.execute("""CREATE TABLE IF NOT EXISTS INVENTORY_ITEMS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            PLAYER_ID INTEGER NOT NULL,
                            NAME TEXT NOT NULL,
                            QUANTITY INTEGER NOT NULL
                        )""")

        connection.commit()
        connection.close()

    def get_player(self, player_id):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM PLAYERS WHERE ID = ?", [player_id])
        result = cursor.fetchone()

        player = Player(result[0], result[1], self.get_player_inventory(player_id))

        connection.commit()
        connection.close()

        return player

    def save_player(self, player):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        # First, checking if the player is already in the database, then adding or updating accordingly:
        cursor.execute("SELECT * FROM PLAYERS WHERE ID = ?", [player.get_id()])
        if len(cursor.fetchall()) > 0:
            # The player is already present, just needs to be updated:
            cursor.execute("UPDATE PLAYERS SET NAME = ? WHERE ID = ?", (player.get_name(), player.get_id()))

            player_id = player.get_id()

        else:
            # The player is not present, needs to be added:
            cursor.execute("INSERT INTO PLAYERS VALUES(NULL, ?)", [player.get_name()])

            # Retrieving the ID of the player such that it can be set to the player instance:
            cursor.execute("SELECT last_insert_rowid()")
            player_id = cursor.fetchone()[0]

            player.set_id(player_id)

        connection.commit()
        connection.close()

        # The inventory of the player also needs to be added:
        self.save_player_inventory(player)

        # Returning the ID of the player just added:
        return player_id

    def get_player_inventory(self, player_id):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM INVENTORY_ITEMS WHERE PLAYER_ID = ?", [player_id])

        inventory = {}

        for item in cursor.fetchall():
            inventory[item[2]] = item[3]

        connection.commit()
        connection.close()

        print(inventory)
        return inventory

    def save_player_inventory(self, player):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        inventory = player.get_inventory()

        for key in inventory:
            # First, checking if the item is in the table, then adding or updating accordingly:
            cursor.execute("SELECT * FROM INVENTORY_ITEMS WHERE NAME = ? AND PLAYER_ID = ?", [key, player.get_id()])
            if len(cursor.fetchall()) > 0:
                # The item is already present, just the quantity needs to be updated:
                cursor.execute("UPDATE INVENTORY_ITEMS SET QUANTITY = ? WHERE NAME = ? AND PLAYER_ID = ?",
                               [inventory[key], key, player.get_id()])
            else:
                # The item is not present, the item itself needs to be added:
                cursor.execute("INSERT INTO INVENTORY_ITEMS VALUES(NULL, ?, ?, ?)",
                               [player.get_id(), key, inventory[key]])

        connection.commit()
        connection.close()

    def get_item_description(self, item_name):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT DESCRIPTION FROM ITEMS WHERE NAME = ?", [item_name])

        result = cursor.fetchone()[0]

        print(result)

        connection.commit()
        connection.close()


Game()
