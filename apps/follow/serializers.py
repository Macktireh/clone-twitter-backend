from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.follow.models import Follow
from apps.profiles.serializers import UserSerializer
from apps.utils.response import error_messages, response_messages


User = get_user_model()
res = response_messages('fr')


class FollowingSerializer(serializers.ModelSerializer):

    user = UserSerializer(source='following', required=False, read_only=True)
    followingPubblicId = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": error_messages('blank', 'fr', 'commentPublicId'),
            "required": error_messages('required', 'fr', 'commentPublicId'),
        },
    )
    # followersPubblicId = serializers.CharField(
    #     write_only=True,
    #     error_messages={
    #         "blank": error_messages('blank', 'fr', 'commentPublicId'),
    #         "required": error_messages('required', 'fr', 'commentPublicId'),
    #     },
    # )
    
    class Meta:
        model = Follow
        exclude = ('id', 'following', 'followers',)
        read_only_fields = ['created', 'updated']
    
    def create(self, validate_data) -> Follow:
        followingPubblicId = validate_data.get('followingPubblicId', None)
        request = self.context.get('request')
        if not followingPubblicId or followingPubblicId is None:
            raise serializers.ValidationError(res["MISSING_PARAMETER"])
        try:
            userfollowing = User.objects.get(public_id=followingPubblicId)
        except:
            raise serializers.ValidationError(res["SOMETHING_WENT_WRONG"])
        if userfollowing is None:
            raise serializers.ValidationError(res["COMMENT_NOT_FOUND"])
        if request.user.public_id == userfollowing.public_id:
            raise serializers.ValidationError("Current user et user followed ne doit pas être égale.")
        follow, is_following = Follow.objects.is_following(request.user, userfollowing)
        if is_following:
            follow.delete()
            return follow
        return Follow.objects.create(followers=request.user, following=userfollowing)



class FollowersSerializer(serializers.ModelSerializer):

    user = UserSerializer(source='followers', required=False, read_only=True)
    # followingPubblicId = serializers.CharField(
    #     write_only=True,
    #     error_messages={
    #         "blank": error_messages('blank', 'fr', 'commentPublicId'),
    #         "required": error_messages('required', 'fr', 'commentPublicId'),
    #     },
    # )
    # followersPubblicId = serializers.CharField(
    #     write_only=True,
    #     error_messages={
    #         "blank": error_messages('blank', 'fr', 'commentPublicId'),
    #         "required": error_messages('required', 'fr', 'commentPublicId'),
    #     },
    # )
    
    class Meta:
        model = Follow
        exclude = ('id', 'following', 'followers')
        read_only_fields = ['created', 'updated']