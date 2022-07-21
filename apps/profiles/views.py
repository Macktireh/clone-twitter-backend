from typing import List
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.decorators import action, api_view, permission_classes, renderer_classes

from apps.account.renderers import UserRenderer
from apps.account.serializers import UserSerializer
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
    
    # @action(detail=True, methods=['put', 'patch'])
    # def user(self, request, pk=None):
    #     try:
    #         if int(pk) != int(request.user.pk):
    #             return Response({'error': {'detail': _("Not Found")}}, status=status.HTTP_404_NOT_FOUND)
    #         profile = self.get_object()
    #         user = profile.user
    #         serializer = UserSerializer(user, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         try:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #         except Exception as e:
    #             return Response({'error': {'detail': _("Not Found")}}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((UserRenderer,))
# def my_profile_view(request):
#     profile = Profile.objects.get(user=request.user)
#     serializer = ProfileSerializer(profile)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET', 'PUT'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((UserRenderer,))
# def my_profile_update_view(request, id):
#     profile = Profile.objects.get(id=id)
#     if request.method == 'PATCH':
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.data.get('user')
#             print(user)
#             # serializer = ProfileSerializer(profile)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'GET':
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)