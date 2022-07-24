from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.post.models import LikePost, Post, Comment
from apps.account.serializers import UserSerializer


User = get_user_model()


class LikePostSerializer(serializers.ModelSerializer):

    author_detail = UserSerializer(read_only=True, source='user')
    postId = serializers.IntegerField(write_only=True)

    class Meta:
        model = LikePost
        fields = ['id', 'value', 'author_detail', 'post', 'postId', 'created']
        extra_kwargs = {
            'id': {'read_only': True},
            'value': {'read_only': True},
            'post': {'read_only': True},
            'created': {'read_only': True},
        }

    def create(self, validate_data):
        post_id = validate_data.get('postId')
        request = self.context.get('request')
        try:
            post_obj = Post.objects.get(id=int(post_id))
        except:
            raise serializers.ValidationError(
                _("Error 404 response")
            )
        if request.user in post_obj.liked.all():
            post_obj.liked.remove(request.user)
        else:
            post_obj.liked.add(request.user)
        like, created = LikePost.objects.get_or_create(user=request.user, post=post_obj)
        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'
        post_obj.save()
        like.save()
        return like


class CommentPostSerializer(serializers.ModelSerializer):

    author_detail = UserSerializer(read_only=True, source='author')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_detail', 'post', 'message', 'created']
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'write_only': True},
            'created': {'read_only': True},
        }


class PostSerializer(serializers.ModelSerializer):

    author_detail = UserSerializer(read_only=True, source='author')
    liked = UserSerializer(read_only=True, many=True)
    comments = CommentPostSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        exclude = ['is_updated']
        extra_kwargs = {
            'author': {'write_only': True},
        }