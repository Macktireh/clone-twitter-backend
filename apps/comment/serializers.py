from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.comment.models import LikeComment, Comment
from apps.profiles.serializers import UserSerializer


User = get_user_model()


class LikeCommentSerializer(serializers.ModelSerializer):

    authorDetail = UserSerializer(read_only=True, source='user')
    publicId = serializers.IntegerField(write_only=True)

    class Meta:
        model = LikeComment
        fields = ['value', 'authorDetail', 'comment', 'publicId']
        read_only_fields = ['value', 'comment']

    def create(self, validate_data):
        public_id = validate_data.get('publicId')
        request = self.context.get('request')
        try:
            comment_obj = Comment.objects.get(public_id=public_id)
        except:
            raise serializers.ValidationError(
                _({'error': {'message': _("Quelque chose a mal tourné !")}})
            )
        if request.user in comment_obj.liked.all():
            comment_obj.liked.remove(request.user)
        else:
            comment_obj.liked.add(request.user)
        like, created = LikeComment.objects.get_or_create(user=request.user, Comment=comment_obj)
        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'
        comment_obj.save()
        like.save()
        return like


class CommentPostSerializer(serializers.ModelSerializer):

    authorDetail = UserSerializer(read_only=True, source='author')
    publicId = serializers.CharField(source='public_id')
    message = serializers.CharField()
    image = serializers.ImageField(required=False)
    liked = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ['publicId', 'authorDetail', 'message', 'image', 'is_updated', 'created', 'updated', 'liked']
        read_only_fields = ['publicId', 'author', 'is_updated', 'created', 'updated', 'liked', 'comments']

    def create(self, validate_data):
        request = self.context.get('request', None)
        message = validate_data.get('message', None)
        image = validate_data.get('image', None)
        if message or image:
            try:
                new_comment = Comment.objects.create(author=request.user, message=message, image=image)
                return new_comment
            except:
                raise serializers.ValidationError({'message': _("Quelque chose a mal tourné !")})
        else:
            raise serializers.ValidationError({'message': _("Le champ message ou image ne doit pas être vide.")})