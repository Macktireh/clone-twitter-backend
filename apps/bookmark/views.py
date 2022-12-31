from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.bookmark.models import Bookmark
from apps.bookmark.serializers import BookmarkSerializer


class BookmarkViewSet(viewsets.ModelViewSet):

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'public_id'
    
    def list(self, request, *args, **kwargs):

        posts = Bookmark.objects.getBookmarksByUser(request.user)
        serializer = BookmarkSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)