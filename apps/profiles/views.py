from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class UserProfileViewSet(viewsets.ModelViewSet):

    parser_classes = (JSONParser, FormParser, MultiPartParser,)
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'patch']
    lookup_field = 'public_id'
    
    def list(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            if not kwargs.get('public_id') == request.user.public_id:
                return Response({'errors': res["MISSING_PARAMETER"]}, status=status.HTTP_404_NOT_FOUND)
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, *args, **kwargs):
        try:
            if kwargs.get('public_id') == request.user.public_id:
                partial = kwargs.pop('partial', False)
                instance = Profile.objects.get(user=request.user)
                serializer = ProfileSerializer(instance, data=request.data, partial=partial)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'errors': res["MISSING_PARAMETER"]}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllUserProfileViewSet(viewsets.ModelViewSet):

    parser_classes = (JSONParser, FormParser, MultiPartParser,)
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    http_method_names = ['get']
    
    def list(self, request):
        users = Profile.objects.get_all_profiles(request.user)
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)