import requests


class YaUploader:
    def __init__(self, tokens: str):
        self.token = tokens

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data.get("href")
        return href

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path)
        response = requests.put(href, data=open(filename, 'rb'))
        if response.status_code == 201:
            print("Success")


if __name__ == '__main__':
    token = "y0_AgAAAAAstFelAADLWwAAAADecfXZMTvrP2p1S2Scr-zqJOfHrfvRqZo"
    ya = YaUploader(tokens=token)
    ya.upload_file_to_disk("learning_exercise/homework.txt", 'file_for_upload.txt')
