from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from apps.utils.renderers import UserRenderer
from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer


User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserRenderer,)
    parser_classes = (JSONParser, FormParser, MultiPartParser,)
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'patch']

    def list(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            if not int(kwargs.get('pk')) == int(request.user.pk):
                return Response({'error': {'detail': _("Not Found")}}, status=status.HTTP_404_NOT_FOUND)
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': {'detail': _("Not Found")}}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            if int(kwargs.get('pk')) == int(request.user.pk):
                partial = kwargs.pop('partial', False)
                instance = Profile.objects.get(user=request.user)
                serializer = ProfileSerializer(instance, data=request.data, partial=partial)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': {'detail': _("Not Found")}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            try:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': {'detail': _("Not Found")}}, status=status.HTTP_404_NOT_FOUND)