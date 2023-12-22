from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import viewsets

from posts.models import Comment, Group, Post
from .serializer import CommentSerializer, GroupSerializer, PostSerializer


class AuthorPermissionMixin:
    def handle_author_permission(self, instance, request):
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        response = self.handle_author_permission(instance, request)
        if not response:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return (
            response
            or Response(serializer.data, status=status.HTTP_200_OK)
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = self.handle_author_permission(instance, request)
        if not response:
            instance.delete()
        return (
            response or Response(status=status.HTTP_204_NO_CONTENT)
        )


class PostViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_post_object_or_404(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        post = self.get_post_object_or_404()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post_object_or_404()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
