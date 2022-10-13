import os
import datetime
import uuid


def rename_img_profile(instance, filename):
    ext = filename.split('.')[-1]
    name = ''
    for i in range((len(filename.split('.'))-1)):
        name += filename.split('.')[i]
    filename = f"{name}_{datetime.datetime.now().strftime('%d-%m-%Y_%H%M%S')}.{ext}"
    folder = f"id-{instance.user.pk}"
    return os.path.join('media', folder, 'profile', filename)

def rename_img_post(instance, filename):
    ext = filename.split('.')[-1]
    name = ''
    for i in range((len(filename.split('.'))-1)):
        name += filename.split('.')[i]
    filename = f"{name}_{datetime.datetime.now().strftime('%d-%m-%Y_%H%M%S')}.{ext}"
    folder = f"id-{instance.author.pk}"
    return os.path.join('media', folder, 'post', filename)

def uid_generator() -> str:
    return str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')