from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import viewsets

from posts.models import Comment, Group, Post
from .serializer import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
