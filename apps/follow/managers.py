from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

from apps.utils.functions import list_to_queryset


User = get_user_model()


class FollowManager(models.Manager):
    def get_all_following(self, user):
        from apps.follow.models import Follow

        return Follow.objects.select_related("following").filter(followers=user)

    def get_all_followers(self, user):
        from apps.follow.models import Follow

        return Follow.objects.select_related("followers").filter(following=user)

    def is_following(self, me, user):
        from apps.follow.models import Follow

        return Follow.objects.filter(
            Q(followers=me) & Q(following=user)
        ), Follow.objects.filter(Q(followers=me) & Q(following=user)).exists()

    def connect_people(self, user):
        from apps.follow.models import Follow

        followers = Follow.objects.get_all_followers(user)
        following = Follow.objects.get_all_following(user)

        list_publicId_follow = [f.followers.public_id for f in followers] + [
            f.following.public_id for f in following
        ]

        users = User.objects.prefetch_related("profile").all()
        people = []

        for u in users:
            if (
                u.public_id not in list(set(list_publicId_follow))
                and u != user
                and u.is_verified_email
                and u.is_active
            ):
                people.append(u)

        qs = list_to_queryset(model=User, data=people)
        return qs.order_by("profile__sort_id")
