from flask import Flask, request
from database_handler import DatabaseHandler, master_db_path, create_master_db
import os, random

"""
Flask Server Code
"""

app = Flask(__name__)

# Maps each username with its corresponding db_handler obj
username_db_map = {}


@app.route('/')
def run_app():
    return '轻橱后端 Flask 服务器加载成功'


@app.route('/add_user', methods=["POST"])
def add_user():
    ret_dict = {'username': None, 'created': None}
    if request.method == "POST":
        # Create the databases
        # Check if we have the database and static folders
        if "database" not in os.listdir(os.getcwd()):
            os.mkdir('database')
        if "static" not in os.listdir(os.getcwd()):
            os.mkdir('static')
        if "users" not in os.listdir("database"):
            os.mkdir(os.path.join("database", "users"))
        # Check if we have created the master directory
        master_dir = master_db_path
        if master_dir not in os.listdir("database"):
            create_master_db()
        data = request.form
        username, first, last = data["username"], data["first"], data["last"]
        gender, dob = data["gender"], data["dob"]
        ret_dict['username'] = username
        try:
            user_db_handler = DatabaseHandler()
            user_db_handler.create_user_database(os.path.join("database", "users"), username)
            user_db_handler.add_user_info(username, first, last, gender, dob)
            username_db_map[username] = user_db_handler
            # Make the dir to store the images
            if 'images' not in os.listdir('static'):
                os.mkdir(os.path.join('static', 'images'))
            ret_dict['created'] = True
        except FileExistsError:
            ret_dict['created'] = False
    return ret_dict


@app.route('/upload_clothing', methods=["POST"])
def upload_clothing():
    ret_dict = {"filename": None, "success": None, "username": None}
    base_url = request.base_url.replace("upload_clothing", "")
    if request.files['photo'].filename:
        try:
            filename = os.path.basename(request.files['photo'].filename)
            clothes_name = request.form['clothes_name']
            username, clothes_type = request.form['username'], request.form['clothes_type']
            ret_dict['username'], ret_dict['filename'] = username, filename
            save_path = os.path.join('static', 'images', f"{username}_{clothes_name}.png")
            image = request.files['photo']
            image.save(save_path)
            image_url = base_url + save_path
            username_db_map[username].add_user_clothes(clothes_name, clothes_type, image_url)
            ret_dict['success'] = True
            ret_dict['url'] = image_url
        except FileNotFoundError:
            ret_dict['success'] = False
            ret_dict['exception'] = "FileNotFound"
    return ret_dict


@app.route('/get_recommendation', methods=["POST"])
def get_recommendation():
    base_url = request.base_url.replace("get_recommendation", "")
    ret_dict = {"username": None, "rec_name": None, "rec_url": None}
    username = request.form['username']
    not_user_items = [c for c in os.listdir(os.path.join('static', 'images')) if not c.startswith(username)]
    rec_name = random.choice(not_user_items)
    ret_dict['rec_name'] = rec_name
    ret_dict['username'] = username
    image_url = os.path.join("static", "images", rec_name)
    ret_dict['rec_url'] = base_url + image_url
    return ret_dict

if __name__ == '__main__':
    app.run()
