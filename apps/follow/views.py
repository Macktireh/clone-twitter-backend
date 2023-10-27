from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status, viewsets

from apps.follow.models import Follow
from apps.follow.serializers import FollowingSerializer, FollowersSerializer
from apps.profiles.serializers import UserSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages("fr")


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.select_related("following").all()
    serializer_class = FollowingSerializer
    http_method_names = ["get", "post"]
    lookup_field = "public_id"

    def list(self, request, *args, **kwargs):
        userPublicId = kwargs.get("userPublicId", None)
        if userPublicId is None:
            return Response(
                {"errors": res["MISSING_PARAMETER"]}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(public_id=userPublicId)
        except User.DoesNotExist:
            return Response(
                {"errors": res["USER_DOES_NOT_EXIST"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow = Follow.objects.get_all_following(user)
        serializer = FollowingSerializer(follow, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowersViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.select_related("followers").all()
    serializer_class = FollowersSerializer
    http_method_names = ["get"]
    lookup_field = "public_id"

    def list(self, request, *args, **kwargs):
        userPublicId = kwargs.get("userPublicId", None)
        if userPublicId is None:
            return Response(
                {"errors": res["MISSING_PARAMETER"]}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(public_id=userPublicId)
        except User.DoesNotExist:
            return Response(
                {"errors": res["USER_DOES_NOT_EXIST"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow = Follow.objects.get_all_followers(user)
        serializer = FollowersSerializer(follow, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PeopleConnectViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get"]
    lookup_field = "public_id"

    def list(self, request):
        people = Follow.objects.connect_people(request.user)
        serializer = UserSerializer(people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
