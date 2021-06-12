import sqlite3
import os


class DatabaseHandler:
    def __init__(self):
        self.db_path = ""

    def create_user_database(self, db_dir, username):
        create_user_table = """CREATE TABLE IF NOT EXISTS "USERINFO" (
            "Username"	TEXT NOT NULL,
            "Firstname"	TEXT NOT NULL,
            "Lastname"	TEXT NOT NULL,
            "Gender"	TEXT NOT NULL,
            "DOB"	    TEXT,
            PRIMARY KEY("Username")
        );"""
        create_clothes_table = """CREATE TABLE IF NOT EXISTS "CLOTHES"  (
            "ID"	INTEGER NOT NULL UNIQUE,
            "ClothesType"	TEXT NOT NULL,
            "URL"	TEXT NOT NULL,
            "Remarks"	TEXT,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );"""
        self.db_path = os.path.join(db_dir, f"{username}.db")
        print(self.db_path)
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(create_user_table)
        cursor.execute(create_clothes_table)
        connection.commit()
        connection.close()

    def add_user_info(self, username, first, last, gender, dob):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        data = cursor.execute(f"SELECT 'Username' FROM 'USERINFO'").fetchall()
        if not data:
            update_userinfo_sql = f"INSERT INTO USERINFO VALUES ('{username}', '{first}','{last}','{gender}','{dob}')"
            cursor.execute(update_userinfo_sql)
        connection.commit()
        connection.close()

    def add_user_clothes(self, clothes_type, image_url, remarks=""):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        update_clothes_sql = f"INSERT INTO CLOTHES ('ClothesType', 'URL', 'Remarks') " \
                             f"VALUES ('{clothes_type}','{image_url}','{remarks}')"
        cursor.execute(update_clothes_sql)
        connection.commit()
        connection.close()