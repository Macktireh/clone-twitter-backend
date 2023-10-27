import cloudinary

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.post.models import LikePost, Post
from apps.comment.models import Comment
from apps.profiles.serializers import UserSerializer
from apps.utils.functions import convert_to_mo
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class LikePostSerializer(serializers.ModelSerializer):
    
    authorDetail = UserSerializer(read_only=True, source='user')
    postPublicId = serializers.CharField(write_only=True)
    PublicId = serializers.CharField(source='post.public_id', read_only=True)
    
    class Meta:
        model = LikePost
        fields = ['value', 'authorDetail', 'PublicId', 'postPublicId', 'created']
        read_only_fields = ['value', 'created']
    
    def create(self, validate_data):
        postPublicId = validate_data.get('postPublicId')
        request = self.context.get('request')
        if not postPublicId or postPublicId is None:
            raise serializers.ValidationError(res["MISSING_PARAMETER"])
        try:
            post_obj = Post.objects.get(public_id=postPublicId) or None
            if post_obj is None:
                raise serializers.ValidationError(res["POST_NOT_FOUND"])
        except:
            raise serializers.ValidationError(res["SOMETHING_WENT_WRONG"])
        if request.user in post_obj.liked.all():
            post_obj.liked.remove(request.user)
        else:
            post_obj.liked.add(request.user)
        like, created = LikePost.objects.get_or_create(user=request.user, post=post_obj)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'
        post_obj.save()
        like.save()
        return like


class BookmarkUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['public_id']
        read_only_fields = ['public_id']


class PostSerializer(serializers.ModelSerializer):
    
    authorDetail = UserSerializer(read_only=True, source='author')
    publicId = serializers.CharField(read_only=True, source='public_id')
    body = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    liked = UserSerializer(read_only=True, many=True)
    numberComments = serializers.SerializerMethodField()
    bookmarks = serializers.SerializerMethodField()
    # bookmarkss = serializers.CharField(read_only=True, source="bookmarks.user.public_id")
    
    def get_numberComments(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    def get_bookmarks(self, obj):
        return [user.public_id for user in obj.bookmarks.all()]
    
    class Meta:
        model = Post
        fields = ['publicId', 'authorDetail', 'body', 'image', 'is_updated', 'created', 'updated', 'liked', 'numberComments', 'bookmarks']
        read_only_fields = ['author', 'is_updated', 'created', 'updated', 'liked', 'comments']
    
    def create(self, validate_data):
        request = self.context.get('request', None)
        body = validate_data.get('body', None)
        image = validate_data.get('image', None)
        
        if body or image:
            try:
                new_post = Post.objects.create(author=request.user, body=body, image=image)
                return new_post
            except cloudinary.exceptions.Error:
                raise serializers.ValidationError({
                    "type": "file size error",
                    "message": f"La taille du fichier est trop grande. J'ai obtenu {convert_to_mo(image.size)} Mo. Le maximum est {convert_to_mo(10485760)} Mo"
                })
            # except:
            #     raise serializers.ValidationError(res["SOMETHING_WENT_WRONG"])
        else:
            raise serializers.ValidationError(res["BODY_OR_IMAGE_FIELD_MUST_NOT_EMPTY"])
    
    def update(self, instance, validated_data):
        body = validated_data.get('body', None)
        image = validated_data.get('image', None)
        
        try:
            if body:
                instance.body = body
            if image:
                instance.image = image
            instance.save()
            return instance
        except cloudinary.exceptions.Error:
                raise serializers.ValidationError({
                    "type": "file size error",
                    "message": f"La taille du fichier est trop grande. J'ai obtenu {convert_to_mo(image.size)} Mo. Le maximum est {convert_to_mo(10485760)} Mo"
                })