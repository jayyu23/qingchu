from flask import request
import requests


def upload_photo(photo_path=None, username=None):
    photo_path = photo_path if photo_path else '002/app005prod-1.png'
    username = username if username else "jayyu2310"
    url = "http://127.0.0.1:5000/upload_photo"
    data = {'user': username}
    files = [('photo', (photo_path, open(photo_path, 'rb'), 'image/png'))]
    r = requests.post(url, data=data, files=files)
    print(r.json())


if __name__ == "__main__":
    upload_photo(photo_path='002/app005prod-9.png', username='jayyu2310')