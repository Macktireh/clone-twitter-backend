from rest_framework import viewsets
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from apps.account.renderers import UserRenderer
from apps.post.models import Post, Comment
from apps.post.serializers import PostSerializer, CommentPostSerializer


class PostViewSet(viewsets.ModelViewSet):
    renderer_classes = (UserRenderer,)
    parser_classes = (JSONParser, FormParser, MultiPartParser,)
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer

class CommentPostViewSet(viewsets.ModelViewSet):
    renderer_classes = (UserRenderer,)
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer
