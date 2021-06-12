from flask import request
import requests


def upload_photo(photo_path=None, user=None):
    photo_path = photo_path if photo_path else '002/app005prod-1.png'
    user = user if user else "jayyu2310"
    url = "http://127.0.0.1:5000/upload_photo"
    files = [('photo', ('app005prod-1.png', open(photo_path, 'rb'), 'image/png'))]
    r = requests.post(url, files=files)
    print(r.json())


if __name__ == "__main__":
    upload_photo()