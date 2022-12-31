from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.bookmark.models import Bookmark


@receiver(post_save, sender=Bookmark)
def bookmark_save(sender, instance, created, **kwargs):
    if not instance.user in instance.post.bookmarks.all():
        instance.post.bookmarks.add(instance.user)
        instance.post.save()

# remove bookmarks from post with pre_delete signal
@receiver(pre_delete, sender=Bookmark)
def bookmark_delete(sender, instance, **kwargs):
    if instance.user in instance.post.bookmarks.all():
        instance.post.bookmarks.remove(instance.user)
        instance.post.save()