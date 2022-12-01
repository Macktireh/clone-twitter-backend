from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth import get_user_model

from apps.follow.models import Follow
from apps.notification.models import Notification, TypeNotif
from apps.post.models import LikePost, Post
from apps.comment.models import Comment, LikeComment


User = get_user_model()


@receiver(post_save, sender=LikePost)
def signals_notification_add_likes_post(sender, instance, created, **kwargs) -> None:
    from_user = instance.user
    to_user = instance.post.author
    if instance.value == 'Like':
        if from_user != to_user:
            Notification.objects.create(
                type_notif=TypeNotif.like_post,
                from_user=from_user,
                to_user=to_user,
                post=instance.post,
                like_post = instance
            )
    else:
        if Notification.objects.filter(like_post=instance).exists():
            notif = Notification.objects.get(like_post=instance)
            notif.delete()


@receiver(post_save, sender=Post)
def signals_notification_add_post(sender, instance, created, **kwargs) -> None:
    from_user = instance.author
    if created:
        followers = Follow.objects.get_all_followers(from_user)
        for f in followers:
            to_user = f.followers
            if from_user != to_user:
                Notification.objects.create(
                    type_notif=TypeNotif.post,
                    from_user=from_user,
                    to_user=to_user,
                    post=instance,
                )


@receiver(post_save, sender=Comment)
def signals_notification_add_comment(sender, instance, created, **kwargs) -> None:
    from_user = instance.author
    to_user = instance.post.author
    if created:
        if from_user != to_user:
            Notification.objects.create(
                type_notif=TypeNotif.comment,
                from_user=from_user,
                to_user=to_user,
                post=instance.post,
                comment_post=instance
            )


@receiver(post_save, sender=LikeComment)
def signals_notification_add_like_comment(sender, instance, created, **kwargs) -> None:
    from_user = instance.user
    to_user = instance.comment.author
    if instance.value == 'Like':
        if from_user != to_user:
            Notification.objects.create(
                type_notif=TypeNotif.like_comment,
                from_user=from_user,
                to_user=to_user,
                post=instance.comment.post,
                comment_post=instance.comment,
                like_comment = instance
            )
    else:
        if Notification.objects.filter(like_comment=instance).exists():
            notif = Notification.objects.get(like_comment=instance)
            notif.delete()


@receiver(post_save, sender=Follow)
def signals_notification_add_follow(sender, instance, created, **kwargs) -> None:
    from_user = instance.following
    to_user = instance.followers
    if created:
        if Notification.objects.filter(type_notif=TypeNotif.following, from_user=to_user, to_user=from_user).exists():
            notif = Notification.objects.get(type_notif=TypeNotif.following, from_user=to_user, to_user=from_user)
            notif.seen = False; notif.read = False
            notif.save()
        else:
            Notification.objects.create(
                type_notif='following',
                from_user=to_user, 
                to_user=from_user
            )


@receiver(pre_delete, sender=Follow)
def signals_notification_delete_follow(sender, instance, **kwargs) -> None:
    from_user = instance.following
    to_user = instance.followers
    
    if Notification.objects.filter(type_notif=TypeNotif.following, from_user=to_user, to_user=from_user).exists():
        notif = Notification.objects.filter(type_notif=TypeNotif.following, from_user=to_user, to_user=from_user)
        notif.delete()