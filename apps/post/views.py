from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from apps.utils.renderers import UserRenderer
from apps.post.models import Post, Comment, LikePost
from apps.post.serializers import PostSerializer, CommentPostSerializer, LikePostSerializer


class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    renderer_classes = [UserRenderer, ]
    parser_classes = [JSONParser, FormParser, MultiPartParser, ]
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer


class CommentPostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    renderer_classes = [UserRenderer, ]
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer


class LikePostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    renderer_classes = [UserRenderer, ]
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer
