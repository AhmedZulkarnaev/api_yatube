from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import viewsets

from posts.models import Comment, Group, Post
from .serializer import CommentSerializer, GroupSerializer, PostSerializer


def check_author(instance, request):
    if instance.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return None


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        response = check_author(instance, request)
        if response:
            return response
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = check_author(instance, request)
        if response:
            return response
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        if post:
            return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        if post:
            serializer.save(author=self.request.user, post_id=post_id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        response = check_author(instance, request)
        if response:
            return response
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = check_author(instance, request)
        if response:
            return response
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
