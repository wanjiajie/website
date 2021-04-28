#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Article, Category_Article, Article_Comment, ArticleCommentReply, Recommend
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','avatar','id')


# class UsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id',)


class Category_ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Article
        fields = ('name','id',)


class Article_CommentSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Article_Comment
        fields = '__all__'


class ArticleCommentReplySerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = ArticleCommentReply
        fields = '__all__'


class ArticleCommentReplySerializerHelper(serializers.ModelSerializer):
    """回复"""
    user = UserSerializer()
    to_uids = UserSerializer()
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = ArticleCommentReply
        fields = '__all__'


class Article_CommentSerializer(serializers.ModelSerializer):
    #评论
    # def to_representation(self, instance):
    #     res=super().to_representation(instance=instance)
    #     if res['aomments_id'] is None:
    #         print(res)
    #         return res
    #     else:
    #         print('ok')
    #         pass
    #         return
    #sub_cat = Article_CommentSerializer1(many=True)
    user = UserSerializer()
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    articlecommentreply_set = ArticleCommentReplySerializerHelper(many=True,read_only=True)

    class Meta:
        model = Article_Comment
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    #文章
    author = UserSerializer()
    category = Category_ArticleSerializer()
    article_comment_set = Article_CommentSerializer(many=True,required=False,read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCommitSerializer(serializers.ModelSerializer):

    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Recommend
        fields = '__all__'
