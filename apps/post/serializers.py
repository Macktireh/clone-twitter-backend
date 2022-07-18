from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.post.models import Post, Comment
from apps.account.serializers import UserSerializer


User = get_user_model()

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