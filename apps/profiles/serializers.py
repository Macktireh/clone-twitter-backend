
from rest_framework import serializers

from apps.profiles.models import Profile
from apps.account.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    birthDate = serializers.DateField(source='birth_date')
    coverPicture = serializers.ImageField(source='cover_picture')
    
    class Meta:
        model = Profile
        exclude = ['id', 'uid', 'birth_date', 'cover_picture', 'created']


# class UpdateProfileSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=150)
#     last_name = serializers.CharField(max_length=150)
#     pseudo = serializers.CharField(max_length=48)
#     birth_date = serializers.DateTimeField()
#     bio = serializers.CharField(max_length=360)
#     profile_pic = serializers.ImageField()
#     cover_pic = serializers.ImageField()
