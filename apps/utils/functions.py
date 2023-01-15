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
    from apps.post.models import Post
    sub_folder = 'post' if isinstance(instance, Post) else 'comment'
    ext = filename.split('.')[-1]
    name = ''
    for i in range((len(filename.split('.'))-1)):
        name += filename.split('.')[i]
    filename = f"{name}_{datetime.datetime.now().strftime('%d-%m-%Y_%H%M%S')}.{ext}"
    folder = f"id-{instance.author.pk}"
    return os.path.join('media', folder, sub_folder, filename)

def uid_generator() -> str:
    return str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')

def list_to_queryset(model, data):
    from django.db.models.base import ModelBase

    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )

    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)


def convert_to_mo(size: int) -> float:
    round(size / (1024 * 1024), 1)