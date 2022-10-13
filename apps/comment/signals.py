from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.comment.models import Comment


@receiver(post_save, sender=Comment)
def post_save_create_profile(sender, instance, created, **kwargs):
    if instance.public_id == "":
        pass