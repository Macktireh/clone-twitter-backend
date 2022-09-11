from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.post.models import LikePost, Post
from apps.profiles.serializers import UserSerializer
from apps.comment.serializers import CommentPostSerializer


User = get_user_model()


class LikePostSerializer(serializers.ModelSerializer):

    authorDetail = UserSerializer(read_only=True, source='user')
    postId = serializers.IntegerField(write_only=True)

    class Meta:
        model = LikePost
        fields = ['value', 'authorDetail', 'post', 'postId', 'created']
        read_only_fields = ['value', 'post', 'created']

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


class PostSerializer(serializers.ModelSerializer):

    authorDetail = UserSerializer(read_only=True, source='author')
    publicId = serializers.CharField(read_only=True, source='public_id')
    body = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    liked = UserSerializer(read_only=True, many=True)
    comments = CommentPostSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['publicId', 'authorDetail', 'body', 'image', 'is_updated', 'created', 'updated', 'liked', 'comments']
        read_only_fields = ['author', 'is_updated', 'created', 'updated', 'liked', 'comments']

    def create(self, validate_data):
        request = self.context.get('request', None)
        body = validate_data.get('body', None)
        image = validate_data.get('image', None)
        print(validate_data)
        if body or image:
            try:
                new_post = Post.objects.create(author=request.user, body=body, image=image)
                return new_post
            except:
                raise serializers.ValidationError({'message': _("Quelque chose a mal tourné !")})
        else:
            raise serializers.ValidationError({'message': _("Le champ body ou image ne doit pas être vide.")})