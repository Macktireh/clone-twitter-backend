from typing import Any

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.comment.models import LikeComment, Comment
from apps.post.models import Post
from apps.profiles.serializers import UserSerializer
from apps.utils.response import error_messages, response_messages


User = get_user_model()
res = response_messages('fr')


class LikeCommentSerializer(serializers.ModelSerializer):

    authorDetail = UserSerializer(read_only=True, source='user')
    commentPublicId = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": error_messages('blank', 'fr', 'commentPublicId'),
            "required": error_messages('required', 'fr', 'commentPublicId'),
        },
    )

    class Meta:
        model = LikeComment
        fields = ['value', 'authorDetail', 'comment', 'commentPublicId']
        read_only_fields = ['value', 'comment']

    def create(self, validate_data) -> LikeComment:
        commentPublicId = validate_data.get('commentPublicId', None)
        request: Any = self.context.get('request')
        if not commentPublicId or commentPublicId is None:
            raise serializers.ValidationError(res["MISSING_PARAMETER"])
        try:
            comment_obj = Comment.objects.get(public_id=commentPublicId) or None
            if comment_obj is None:
                raise serializers.ValidationError(res["COMMENT_NOT_FOUND"])
        except:
            raise serializers.ValidationError(res["SOMETHING_WENT_WRONG"])
        if request.user in comment_obj.liked.all():
            comment_obj.liked.remove(request.user)
        else:
            comment_obj.liked.add(request.user)
        like, created = LikeComment.objects.get_or_create(user=request.user, comment=comment_obj)
        if not created:
            if like.value=='Like':
                like.value='Unlike'
                comment_obj.save()
                like.delete()
                return like
            else:
                like.value='Like'
        else:
            like.value='Like'
        comment_obj.save()
        like.save()
        return like


class CommentPostSerializer(serializers.ModelSerializer):

    authorDetail = UserSerializer(read_only=True, source='author')
    postPublicId = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": error_messages('blank', 'fr', 'postPublicId'),
            "required": error_messages('required', 'fr', 'postPublicId'),
        },
    )
    postPublicIdRead = serializers.CharField(
        read_only=True,
        source='post.public_id',
    )
    publicId = serializers.CharField(read_only=True, source='public_id')
    message = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    liked = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ['publicId', 'postPublicIdRead', 'authorDetail', 'postPublicId', 'message', 'image', 'is_updated', 'created', 'updated', 'liked']
        read_only_fields = ['author', 'is_updated', 'created', 'updated', 'liked', 'comments']

    def create(self, validate_data) -> Comment:
        request: Any = self.context.get('request', None)
        postPublicId = validate_data.get('postPublicId', None)
        message = validate_data.get('message', None)
        image = validate_data.get('image', None)
        if message or image:
            try:
                post = Post.objects.get(public_id=postPublicId)
                new_comment = Comment.objects.create(author=request.user, post=post, message=message, image=image)
                return new_comment
            except:
                raise serializers.ValidationError(res["SOMETHING_WENT_WRONG"])
        else:
            raise serializers.ValidationError(res["MESSAGE_OR_IMAGE_FIELD_MUST_NOT_EMPTY"])