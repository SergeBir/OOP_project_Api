import requests
import os
from downloading_photos import Vkontakte


class YaUploader:
    def __init__(self, tokens: str):
        self.token = tokens
        self.vko = Vkontakte()
        self.photos_dir = "photos"

    def create_folder(self, disk_folder_path):
        create_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {"path": disk_folder_path}
        response = requests.put(create_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f"Folder '{disk_folder_path}' created successfully")

    def get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        if 'href' in data:
            href = data.get("href")
            return href
        else:
            self.create_folder(disk_file_path)
            response = requests.get(upload_url, headers=headers, params=params)
            data = response.json()
            href = data.get("href")
            return href

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self.get_upload_link(disk_file_path=disk_file_path)
        response = requests.put(href, data=open(filename, 'rb'))
        if response.status_code == 201:
            print("Success")

    def start_uploading(self):
        self.vko.get_photos()
        ya = YaUploader(tokens=self.token)
        ya.create_folder("api_vk_homework")
        photos = os.listdir(self.photos_dir)
        for photo in photos:
            photo_path = os.path.join(self.photos_dir, photo)
            ya.upload_file_to_disk("api_vk_homework/" + photo, photo_path)
