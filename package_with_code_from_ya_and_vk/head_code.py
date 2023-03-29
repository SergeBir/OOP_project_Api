from uploading_photos import YaUploader
"""В этом файле запускается основной код"""

uploader = YaUploader(tokens=input("Введите токен от Яндекс.Диска: "))
uploader.start_uploading()