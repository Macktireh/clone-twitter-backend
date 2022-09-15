from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.profiles.models import Profile
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')

class UserSerializer(serializers.ModelSerializer):

    # firstName = serializers.CharField(source='first_name')
    # lastName = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ['public_id', 'first_name', 'last_name']
        read_only_fields = ['public_id']


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)
    pseudo = serializers.CharField(validators=[UniqueValidator(queryset=Profile.objects.all(), lookup='iexact')])
    birthDate = serializers.DateField(source='birth_date')
    profilePicture = serializers.ImageField(source='profile_picture')
    coverPicture = serializers.ImageField(source='cover_picture')

    class Meta:
        model = Profile
        exclude = ['id', 'birth_date', 'profile_picture', 'cover_picture']
        read_only_fields = ['created', 'updated']

    def update(self, instance, validated_data):
        try:
            if validated_data.get('user'):
                user_data = validated_data.pop('user')
                user_ser = UserSerializer(instance=instance.user, data=user_data)
                if user_ser.is_valid():
                    user_ser.save()
            instance.pseudo = validated_data.get('pseudo', instance.pseudo)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
            instance.cover_picture = validated_data.get('cover_picture', instance.cover_picture)
            instance.save()
            return instance
        except:
            raise serializers.ValidationError(res["USER_DOES_NOT_EXIST"])