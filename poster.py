from flask import request
import requests


def upload_photo(photo_path: str):
    photo_path = photo_path if photo_path else '002/app005prod-1.png'
    url = "127.0.0.1:5000"
    files = [('images', open(photo_path, 'rb'), 'image/png')]
    r = requests.post(url, files=files)