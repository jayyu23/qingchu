import sqlite3
import os


class DatabaseHandler:
    def __init__(self):
        self.db_path = ""

    def create_user_database(self, db_dir, username):
        create_user_table = """CREATE TABLE "USERINFO" (
            "Username"	TEXT NOT NULL,
            "Firstname"	TEXT NOT NULL,
            "Lastname"	TEXT NOT NULL,
            "Gender"	TEXT NOT NULL,
            "DOB"	NUMERIC,
            PRIMARY KEY("ID")
        );"""
        create_clothes_table = """CREATE TABLE "CLOTHES" (
            "ID"	INTEGER NOT NULL UNIQUE,
            "ClothesType"	TEXT NOT NULL,
            "URL"	TEXT NOT NULL,
            "Remarks"	TEXT,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );"""
        self.db_path = os.path.join(db_dir, username)
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(create_user_table)
        cursor.execute(create_clothes_table)
        connection.commit()
        connection.close()

    def update_user_info(self, username, first, last, gender, dob):
        cursor = sqlite3.connect(self.db_path).cursor()
        cursor.execute(f"""UPDATE USERINFO SET Username = '{username}',
                                               Firstname = '{first}',
                                               Lastname = '{last}',
                                               Gender = '{gender}'
                                               DOB = '{dob}'""")

