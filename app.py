from flask import Flask, request, url_for
import sqlite3
import os

app = Flask(__name__)

"""
Flask Server Code
"""

@app.route('/')
def run_app():
    BASE_URL = request.base_url
    return 'Flask Server Started'


@app.route('/add_user', methods=["POST"])
def add_user():
    # http://127.0.0.1:5000/add_user?user_id=123456
    ret_dict = {'user_id': None, 'success': None}
    if request.method == "POST":
        pass
    data = request.args
    if 'user_id' in data:
        user_id = data['user_id']
        ret_dict['user_id'] = user_id
        if 'users' not in os.listdir('static'):
            os.mkdir(os.path.join('static', 'users'))
        try:
            # Make dir for the user
            os.mkdir(os.path.join('static', 'users', user_id))
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
