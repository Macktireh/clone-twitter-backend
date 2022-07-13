from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.account.renderers import UserRenderer
from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer


User = get_user_model()

class GetUserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)