import sqlite3
import os

master_db_path = os.path.join("database", "master.db")


def create_master_db():
    create_master_sql = """CREATE TABLE IF NOT EXISTS "USERINFO" (
            "Username"	TEXT NOT NULL,
            "Firstname"	TEXT NOT NULL,
            "Lastname"	TEXT NOT NULL,
            "Gender"	TEXT NOT NULL,
            "DOB"	    TEXT,
            PRIMARY KEY("Username")
        );"""
    connection = sqlite3.connect(master_db_path)
    cursor = connection.cursor()
    cursor.execute(create_master_sql)
    connection.commit()
    connection.close()


def execute_master_sql(sql_string):
    connection = sqlite3.connect(master_db_path)
    cursor = connection.cursor()
    results = tuple(cursor.execute(sql_string).fetchall())
    connection.commit()
    connection.close()
    return results


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
            "ClothesName"	TEXT NOT NULL UNIQUE,
            "ClothesType"	TEXT NOT NULL,
            "URL"	TEXT NOT NULL,
            "Remarks"	TEXT,
            PRIMARY KEY("ClothesName")
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
        # Add information into the master database
        master_connection = sqlite3.connect(master_db_path)
        master_cursor = master_connection.cursor()
        master_data = master_cursor.execute(f"SELECT Username FROM 'USERINFO' WHERE Username='{username}'").fetchall()
        if not master_data:
            update_master_sql = f"INSERT INTO USERINFO VALUES ('{username}', '{first}','{last}','{gender}','{dob}')"
            master_cursor.execute(update_master_sql)
        master_connection.commit()
        master_connection.close()

    def add_user_clothes(self, clothes_name, clothes_type, image_url, remarks=""):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        update_clothes_sql = f"INSERT INTO CLOTHES ('ClothesName', 'ClothesType', 'URL', 'Remarks') " \
                             f"VALUES ('{clothes_name}', '{clothes_type}','{image_url}','{remarks}')"
        cursor.execute(update_clothes_sql)
        connection.commit()
        connection.close()

    def get_all_images(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        results = tuple(cursor.execute("SELECT ClothesName, ClothesType, URL FROM CLOTHES").fetchall())
        connection.commit()
        connection.close()
        return results



