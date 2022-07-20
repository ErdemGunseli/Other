import os
import sqlite3
from player import *


class DatabaseHelper:

    # Constants for the type of setting:
    FRAME_RATE_LIMIT = 0
    SHOW_FRAME_RATE = 1
    AUDIO_VOLUME = 2

    def __init__(self):
        # Name of the relational database:
        self.database = "database.db"

        # Checking if the database already exists, no need to set it up again:
        if os.path.isfile(self.database): return


        # Creating database tables:
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # Settings Table:
        cursor.execute("""CREATE TABLE IF NOT EXISTS SETTINGS(
                            TYPE INTEGER PRIMARY KEY NOT NULL,
                            VALUE REAL NOT NULL
                            )""")

        # Default values for settings:
        cursor.executemany("INSERT INTO SETTINGS VALUES(?, ?)",
                           [(self.FRAME_RATE_LIMIT, 60),
                            (self.SHOW_FRAME_RATE, 0),
                            (self.AUDIO_VOLUME, 0.5)])

        # Levels Table:
        connection.execute("""CREATE TABLE IF NOT EXISTS LEVELS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT NOT NULL,
                            FOLDER_PATH TEXT NOT NULL 
                            )""")

        # Inserting levels:
        cursor.executemany("INSERT INTO LEVELS VALUES(NULL, ?, ?)",
                           [("Test Map", "level_maps/test_map.tmx")])

        # Player Stats Table:
        cursor.execute("""CREATE TABLE PLAYER_STATS(
                            TYPE INTEGER PRIMARY KEY NOT NULL,
                            VALUE REAL
                            )""")

        cursor.executemany("INSERT INTO PLAYER_STATS VALUES(?, 0)",
                           [(Player.CURRENT_LEVEL_ID,),
                            (Player.MAX_HEALTH,),
                            (Player.CURRENT_HEALTH,),
                            (Player.RUN_SPEED,),
                            (Player.MELEE_DAMAGE,),
                            (Player.RANGED_DAMAGE,),
                            (Player.DAYS_SURVIVED,),
                            (Player.KILLS,)])

        connection.commit()
        connection.close()

    def get_setting(self, setting_type):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # Retrieving desired setting:
        cursor.execute("SELECT VALUE FROM SETTINGS WHERE TYPE=?", [setting_type])

        cursor_return = cursor.fetchone()
        if cursor_return is not None:
            result = float(cursor_return[0])
        else:
            result = None

        connection.commit()
        connection.close()

        return result

    def update_setting(self, setting_type, value):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # Updating the record (we know it exists since we added default values in constructor):
        cursor.execute("UPDATE SETTINGS SET VALUE = ? WHERE TYPE = ? ", [value, setting_type])

        connection.commit()
        connection.close()

    def get_level_path(self, level_id):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # Retrieving desired level path:
        cursor.execute("SELECT FOLDER_PATH FROM LEVELS WHERE ID=?", [level_id])

        cursor_return = cursor.fetchone()
        if cursor_return is not None:
            path = cursor_return[0]
        else:
            path = None

        connection.commit()
        connection.close()

        return path

    def get_player_stats(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # Retrieving desired level:
        cursor.execute("SELECT * FROM PLAYER_STATS")

        cursor_return = cursor.fetchall()
        if cursor_return[0] is not None:

            stats = {}
            for item in cursor_return:
                stats[item[0]] = item[1]

        else:
            stats = None

        connection.commit()
        connection.close()

        return stats

    def update_player_stats(self, player):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        stats = player.get_stats()

        for key in stats:
            cursor.execute("UPDATE PLAYER_STATS SET VALUE=? WHERE TYPE=?", [stats[key], key])


        connection.commit()
        connection.close()


