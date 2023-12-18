from rest_framework import serializers

from posts.models import Post, Comment, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        read_only_fields = ('pub_date', 'author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
