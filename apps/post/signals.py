from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.post.models import Post


@receiver(post_save, sender=Post)
def post_save_create_profile(sender, instance, created, **kwargs):
    if instance.public_id == "":
        pass