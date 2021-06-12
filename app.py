from flask import Flask, request
import os

app = Flask(__name__)


@app.route('/')
def run_app():
    return 'Flask Server Started'


@app.route('/add_user')
def add_user():
    # http://127.0.0.1:5000/add_user?user_id=123456
    data = request.args
    ret_dict = {'user_id': None, 'success': None}
    if 'user_id' in data:
        user_id = data['user_id']
        ret_dict['user_id'] = user_id
        try:
            # Make dir for the user
            os.mkdir(os.path.join('users', user_id))
            ret_dict['success'] = True
        except FileExistsError:
            ret_dict['success'] = False
    return ret_dict


@app.route('/upload_photo', methods=["POST"])
def upload_photo():
    if request.method == "POST":
        pass


if __name__ == '__main__':
    app.run()
