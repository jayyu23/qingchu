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
    ret_dict = {'username': None, 'success': None}
    if request.method == "POST":
        # Create the databases
        data = request.form
        username, first, last = data["username"], data["first"], data["last"]
        gender, dob = data["gender"], data["dob"]
        user_db_handler = DatabaseHandler()
        user_db_handler.create_user_database("database", username)
        user_db_handler.update_user_info(username, first, last, gender, dob)
        username_db_map[username] = user_db_handler
        # Make the dir to store the images
        if 'users' not in os.listdir('static'):
            os.mkdir(os.path.join('static', 'users'))
        try:
            # Make dir for the user
            os.mkdir(os.path.join('static', 'users', username))
            ret_dict['success'] = True
        except FileExistsError:
            ret_dict['success'] = False
    return ret_dict

@app.route('/upload_photo', methods=["POST"])
def upload_photo():
    ret_dict = {"filename": None, "success": None, "user": None}
    if request.method == "POST":
        base_url = request.base_url.removesuffix("upload_photo")
        if request.files['photo'].filename:
            try:
                filename = os.path.basename(request.files['photo'].filename)
                user_id = request.form['user']
                ret_dict['user'], ret_dict['filename'] = user_id, filename
                save_path = os.path.join('static', 'users', user_id, filename)
                photo = request.files['photo']
                photo.save(save_path)
                ret_dict['success'] = True
                ret_dict['url'] = base_url + save_path  # url_for('run_app', _external=True)
            except FileNotFoundError:
                ret_dict['success'] = False
                ret_dict['exception'] = "FileNotFound"
    return ret_dict


if __name__ == '__main__':
    app.run()
