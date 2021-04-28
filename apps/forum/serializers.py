from rest_framework import serializers

from apps.article.serializers import UserSerializer
from apps.forum.models import Forum_template, Forum, Comment, Parent_Comment


class Forum_templateSerializers(serializers.ModelSerializer):
    #author = UserSerializer(read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Forum_template
        fields ='__all__'


class Parent_CommentSerializersHelper(serializers.ModelSerializer):
    """
    评论回复
    """
    class Meta:
        model = Parent_Comment
        fields = '__all__'


class CommentSerializers(serializers.ModelSerializer):
    """
    评论
    """
    parent_comment_set=Parent_CommentSerializersHelper(many=True)
    class Meta:
        model = Comment
        fields = '__all__'


class ForumSerializers(serializers.ModelSerializer):
    """帖子"""
    author = UserSerializer(read_only=True)
    category = Forum_templateSerializers(read_only=True)
    comment_set = CommentSerializers(many=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Forum
        fields ='__all__'


class Parent_CommentSerializers(serializers.ModelSerializer):
    """
    评论回复
    """
    #parent_comments = CommentSerializers()
    user = UserSerializer(read_only=True)
    to_Parent_Comment = UserSerializer(read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Parent_Comment
        fields = '__all__'

class CommentSerializers(serializers.ModelSerializer):
    """
    评论列表
    """
    user = UserSerializer(read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    parent_comment_set = Parent_CommentSerializers(many=True)
    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializersAdd(serializers.ModelSerializer):
    """
    评论新增
    """
    class Meta:
        model = Comment
        fields = '__all__'

class ForumSerializers(serializers.ModelSerializer):
    """帖子列表"""
    author = UserSerializer(read_only=True)
    category = Forum_templateSerializers(read_only=True)
    comment_set = CommentSerializers(many=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Forum
        fields ='__all__'
