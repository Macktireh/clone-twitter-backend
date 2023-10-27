import cloudinary

from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from apps.post.models import Post, LikePost
from apps.post.serializers import PostSerializer, LikePostSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages("fr")

if settings.ENV == "production":
    cloudinary.config(**settings.CLOUDINARY_STORAGE)


class PostViewSet(viewsets.ModelViewSet):
    parser_classes = [
        JSONParser,
        FormParser,
        MultiPartParser,
    ]
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    lookup_field = "public_id"

    def update(self, request, *args, **kwargs):
        try:
            public_id = kwargs.get("public_id", None)
            if public_id:
                instance = Post.objects.get(public_id=public_id)
                if not instance.author == request.user:
                    return Response(
                        {"errors": res["YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION"]},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                partial = kwargs.pop("partial", False)
                if request.data.get("image", None) is not None:
                    if len(str(instance.image)) != 0 and instance.image and settings.ENV == "production":
                        cloudinary.uploader.destroy(str(instance.image))
                serializer = PostSerializer(
                    instance, data=request.data, partial=partial
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"errors": res["MISSING_PARAMETER"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except cloudinary.exceptions.Error:
            return Response(
                {"errors": res["FILE_SIZE_TOO_LARGE"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # except:
        #     return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            public_id = kwargs.get("public_id", None)
            if public_id:
                instance = Post.objects.get(public_id=public_id)
                if not instance.author == request.user:
                    return Response(
                        {"errors": res["YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION"]},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                if len(str(instance.image)) != 0 and instance.image and settings.ENV == "production":
                    cloudinary.uploader.destroy(str(instance.image))
                self.perform_destroy(instance)
                return Response(status=status.HTTP_200_OK)
            return Response(
                {"errors": res["MISSING_PARAMETER"]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {"errors": res["SOMETHING_WENT_WRONG"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LikePostViewSet(viewsets.ModelViewSet):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer
    http_method_names = ["get", "post"]
    lookup_field = "public_id"


class ListPostsLikesViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        public_id = kwargs.get("userPublicId", None)
        if not public_id:
            return Response(
                {"errors": res["MISSING_PARAMETER"]}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(public_id=public_id)
        except Exception:
            return Response(
                {"errors": res["SOMETHING_WENT_WRONG"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        posts = Post.objects.get_posts_like(user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
