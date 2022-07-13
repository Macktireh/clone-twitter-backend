import os
import datetime
import uuid


def rename_img(instance, filename, sub_folder_img):
    ext = filename.split('.')[-1]
    name = ''
    for i in range((len(filename.split('.'))-1)):
        name += filename.split('.')[i]
    filename = f"{name}_{datetime.datetime.now().strftime('%d-%m-%Y_%H%M%S')}.{ext}"
    folder = f"{instance.user.pk}-{instance.user.first_name}-{instance.user.last_name}"
    return os.path.join('media', folder, sub_folder_img, filename)

def profile_img(instance, filename, sub_folder_img='profile'):
    rename_img(instance, filename, sub_folder_img)

def uid_gerator(id) -> str:
    uid = str(uuid.uuid4()).replace('-', '') + str(id) + str(uuid.uuid4()).replace('-', '')+ str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '') + str(id) + str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')
    return str(uid)