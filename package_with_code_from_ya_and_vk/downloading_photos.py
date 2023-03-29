import vk_api
import json
import os


class Vkontakte:
    def __init__(self):
        pass

    def get_photos(self):
        vk_session = vk_api.VkApi(token=input('Введите ваш_токен_VK: '))
        vk = vk_session.get_api()

        photos = vk.photos.get(owner_id=input('Введите идентификатор_пользователя: '), album_id='profile')

        sorted_photos = sorted(photos['items'], key=lambda p: (-p.get('likes', {}).get('count', 0), p['date']))

        if not os.path.exists('photos'):
            os.makedirs('photos')

        photo_info = []
        for i, photo in enumerate(sorted_photos):
            try:
                filename = f"{photo['likes'].get('count', 0)}_{photo['date']}.jpg"
            except KeyError:
                filename = f"0_{photo['date']}.jpg"
            with open(f"photos/{filename}", 'wb') as f:
                f.write(vk_session.http.get(photo['sizes'][-1]['url']).content)

            photo_info.append({
                'id': photo['id'],
                'likes': photo.get('likes', {}).get('count', 0),
                'date': photo['date'],
                'filename': filename
            })

        with open('photos/photo_info.json', 'w') as f:
            json.dump(photo_info, f)


if __name__ == "__main__":
    vk = Vkontakte()
    vk.get_photos()
