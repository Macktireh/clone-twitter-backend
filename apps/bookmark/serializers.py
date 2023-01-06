from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.bookmark.models import Bookmark
from apps.post.models import Post
from apps.post.serializers import PostSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class BookmarkSerializer(serializers.ModelSerializer):
    
    postPublicId = serializers.CharField(write_only=True)
    userPublicId = serializers.CharField(source='user.public_id', read_only=True)
    posts = PostSerializer(source='post', read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['postPublicId', 'userPublicId', 'posts']
    
    def create(self, validate_data):
        postPublicId = validate_data.get('postPublicId')
        request = self.context.get('request')
        if not postPublicId or postPublicId is None:
            raise serializers.ValidationError(res["MISSING_PARAMETER"])
        try:
            post = Post.objects.get(public_id=postPublicId) or None
            if post is None:
                raise serializers.ValidationError(res["POST_NOT_FOUND"])
        except:
            raise serializers.ValidationError(res["SOMETHING_WENT_WRONG"])
        
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        if not created:
            bookmark.delete()
        return bookmark