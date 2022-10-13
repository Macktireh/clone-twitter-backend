from django.utils.translation import gettext as _

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from apps.comment.models import Comment, LikeComment
from apps.post.models import Post
from apps.comment.serializers import CommentPostSerializer, LikeCommentSerializer
from apps.utils.response import response_messages


res = response_messages('fr')

class CommentPostViewSet(viewsets.ModelViewSet):

    parser_classes = [JSONParser, FormParser, MultiPartParser, ]
    queryset = Comment.objects.select_related('author').all()
    serializer_class = CommentPostSerializer
    lookup_field = 'public_id'
    
    def list(self, request, *args, **kwargs):
        postPublicId = kwargs.get('postPublicId', None)
        if not postPublicId:
            return Response({'errors': res["POST_NOT_FOUND"]}, status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.get(public_id=postPublicId)
        except:
            return Response({'errors': res["YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION"]}, status=status.HTTP_403_FORBIDDEN)
        if not post:
            return Response({'errors': res["POST_NOT_FOUND"]}, status=status.HTTP_404_NOT_FOUND)
        try:
            comments = Comment.objects.filter(post=post)
            serializer = CommentPostSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            public_id = kwargs.get('public_id', None)
            if public_id:
                instance = Comment.objects.get(public_id=public_id)
                if not instance.author == request.user:
                    return Response({'errors': res["YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION"]}, status=status.HTTP_403_FORBIDDEN)
                partial = kwargs.pop('partial', False)
                serializer = CommentPostSerializer(instance, data=request.data, partial=partial)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'errors': res["MISSING_PARAMETER"]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            public_id = kwargs.get('public_id', None)
            if public_id:
                instance = Comment.objects.get(public_id=public_id)
                if instance.author == request.user:
                    self.perform_destroy(instance)
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response({'errors': res["YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION"]}, status=status.HTTP_403_FORBIDDEN)
            return Response({'errors': res["MISSING_PARAMETER"]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class LikeCommentViewSet(viewsets.ModelViewSet):

    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer