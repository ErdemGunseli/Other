import sqlite3

class DatabaseHelper:

    def __init__(self):
        self.DATABASE = "database.db"
        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS DATA(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        DESCRIPTION TEXT,
                        VALUE INTEGER
                    )""")

        connection.commit()
        connection.close()

    def add_item(self, args):
        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.executemany("INSERT INTO DATA VALUES(NULL, ?, ?)", args)

        connection.commit()
        connection.close()

    def get_item(self, item_id):
        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM DATA WHERE ID = ?", str(item_id))

        result = cursor.fetchall()

        connection.close()

        return result

    def update_value(self, item_id, value):
        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("UPDATE DATA SET VALUE = ? WHERE ID = ?", (value, item_id))

        connection.commit()
        connection.close()

    def delete_value(self, item_id):
        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM DATA WHERE ID = ?", str(item_id))

        connection.close()

    def delete_all(self):
        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM DATA")

        connection.close()

    def get_some(self, limit):

        if limit < 1:
            return []

        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM DATA ORDER BY DESCRIPTION ASC LIMIT ? ", str(int(limit)))

        result = cursor.fetchall()

        connection.close()

        return result

    def get_all(self):

        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM DATA ORDER BY DESCRIPTION ASC")

        result = cursor.fetchall()

        connection.close()

        return result

    def delete_data(self):
        connection = sqlite3.connect(self.DATABASE)
        cursor = connection.cursor()

        cursor.execute("DROP TABLE DATA")

        connection.commit()
        connection.close()


databaseHelper = DatabaseHelper()
databaseHelper.add_item([("Value - D", 69)])
databaseHelper.add_item([("Value - A", 69), ("Value - Z", 69)])
databaseHelper.add_item([("Value - F", 69)])
databaseHelper.add_item([("Value - G", 69)])
databaseHelper.add_item([("Value - Y", 69)])
print("First:{}".format(databaseHelper.get_item(1)))
databaseHelper.update_value(1, 6969)
databaseHelper.delete_value(1)

for item in databaseHelper.get_all():
    print(item)

print("\n" + "-" * 10 + "\n")

for item in databaseHelper.get_some(4):
    print(item)

# databaseHelper.delete_all()
print("Final: {}".format(databaseHelper.get_all()))
# databaseHelper.delete_data()
