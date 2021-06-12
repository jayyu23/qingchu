from flask import request
import requests
import os
"""
Module simulates a Client
"""


def upload_photo(photo_path=None, username=None):
    photo_path = photo_path if photo_path else '002/app005prod-1.png'
    username = username if username else "jayyu2310"
    url = "http://127.0.0.1:5000/upload_photo"
    data = {'user': username}
    files = [('photo', (photo_path, open(photo_path, 'rb'), 'image/png'))]
    r = requests.post(url, data=data, files=files)
    print(r.json())


def add_user(user_name):
    data = {"username": "archronac", "first": "Jay", "last": "Yu", "gender": "M", "dob": "1999-12-31"}
    url = "http://127.0.0.1:5000/add_user"
    r = requests.post(url, data=data)
    print(r.json())


if __name__ == "__main__":
    user_data_map = {"jeff3ries": "001",
                     "jillsmith67": "002",
                     "velvetrose": "003",
                     "sandy.young": "004",
                     "lachlanite564": "005"}
    for user, folder in user_data_map.items():
        add_user(user)
        user_fol = os.path.join('input_test', folder)
        for im in os.listdir(user_fol):
            path = os.path.join(user_fol, im)
            upload_photo(photo_path=path, username=user)