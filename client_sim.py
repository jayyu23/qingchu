import requests
import os
import random

"""
Module simulates a Client
"""

root_url_online = "http://qingchu.pythonanywhere.com/"
root_url_local = "http://127.0.0.1:5000/"
root_url = root_url_online


def upload_clothing(photo_path=None, username=""):
    clothes_types = ['shirt', 'pants', 'dress', 'shoes']
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    clothes_name = "".join([random.choice(alphabet) for c in range(8)])
    print(clothes_name)
    files = {'photo': open(photo_path, 'rb')}
    values = {'username': username, 'clothes_type': random.choice(clothes_types), 'clothes_name': clothes_name}
    url = root_url + "upload_clothing"
    r = requests.post(url, data=values, files=files)
    print(r.json())


def add_user(user_data):
    url = root_url + "add_user"
    print(url)
    r = requests.post(url, data=user_data)
    print(r.json())


def get_recommendation(username):
    # Get a recommendation for a given user
    url = root_url + "get_recommendation"
    r = requests.post(url, data={"username": username})
    print(r.json())

if __name__ == "__main__":
    users = [{"username": "jeff3ries", "first": "Jeff", "last": "Huang", "gender": "M", "dob": "1997-08-01"},
             {"username": "jillsmith67", "first": "Jill", "last": "Smith", "gender": "F", "dob": "2003-10-31"},
             {"username": "velvetrose", "first": "Val", "last": "Flemings", "gender": "F", "dob": "1996-05-05"},
             {"username": "sandy.young", "first": "Sandy", "last": "Young", "gender": "F", "dob": "1988-12-18"},
             {"username": "lachlanite564", "first": "Lachlan", "last": "McGee", "gender": "M", "dob": "1994-12-31"},]
    user_photos_map = {"jeff3ries": "001",
                     "jillsmith67": "002",
                     "velvetrose": "003",
                     "sandy.young": "004",
                     "lachlanite564": "005"}
    for u in users:
        name = u['username']
        u_folder = os.path.join('input_test', user_photos_map[name])
        add_user(u)
        for im in os.listdir(u_folder):
            if im[0] == ".":
                continue
            path = os.path.join(u_folder, im)
            upload_clothing(photo_path=path, username=name)

    # Output the recommendations
    for i in users:
        get_recommendation(i['username'])