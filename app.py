from flask import Flask, request, url_for
from database_handler import DatabaseHandler
import os

"""
Flask Server Code
"""

app = Flask(__name__)

# Maps each username with its corresponding db_handler obj
username_db_map = {}


@app.route('/')
def run_app():
    BASE_URL = request.base_url
    return 'Flask Server Started'


@app.route('/add_user', methods=["POST"])
def add_user():
    ret_dict = {'username': None, 'created': None}
    if request.method == "POST":
        # Create the databases
        data = request.form
        username, first, last = data["username"], data["first"], data["last"]
        gender, dob = data["gender"], data["dob"]
        ret_dict['username'] = username
        user_db_handler = DatabaseHandler()
        user_db_handler.create_user_database("database", username)
        user_db_handler.add_user_info(username, first, last, gender, dob)
        username_db_map[username] = user_db_handler
        # Make the dir to store the images
        if 'users' not in os.listdir('static'):
            os.mkdir(os.path.join('static', 'users'))
        try:
            # Make dir for the user
            os.mkdir(os.path.join('static', 'users', username))
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
            username, clothes_type = request.form['username'], request.form['clothes_type']
            ret_dict['username'], ret_dict['filename'] = username, filename
            save_path = os.path.join('static', 'users', username, filename)
            image = request.files['photo']
            image.save(save_path)
            image_url = base_url + save_path
            username_db_map[username].add_user_clothes(clothes_type, image_url)
            ret_dict['success'] = True
            ret_dict['url'] = image_url
        except FileNotFoundError:
            ret_dict['success'] = False
            ret_dict['exception'] = "FileNotFound"
    return ret_dict


if __name__ == '__main__':
    app.run()
