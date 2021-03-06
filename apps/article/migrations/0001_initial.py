# Generated by Django 3.1.7 on 2021-04-18 21:32

import apps.article.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('keywords', models.CharField(blank=True, max_length=200, null=True)),
                ('desc', models.CharField(blank=True, max_length=256, null=True)),
                ('list_pic', models.ImageField(blank=True, null=True, upload_to=apps.article.models.article_directory_path)),
                ('content', models.TextField()),
                ('click_nums', models.IntegerField(default=0, verbose_name='阅读数量')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='Article_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(verbose_name='评论')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='地址')),
                ('url', models.CharField(blank=True, default='', max_length=60, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article', verbose_name='文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '文章评论',
                'verbose_name_plural': '文章评论',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='Category_Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Headlines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('category', models.CharField(max_length=20, verbose_name='分类')),
                ('content', models.TextField(default='', verbose_name='内容')),
                ('author_name', models.CharField(max_length=100, verbose_name='来源')),
                ('url', models.URLField(verbose_name='地址')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='是否推荐')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('recommends', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.article')),
            ],
            options={
                'verbose_name': '文章推荐',
                'verbose_name_plural': '文章推荐',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='ArticleCommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(verbose_name='回复内容')),
                ('url', models.CharField(blank=True, default='', max_length=60, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='地址')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('comments_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article_comment', verbose_name='回复id')),
                ('to_uids', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='to_uids', to=settings.AUTH_USER_MODEL, verbose_name='目标用户')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_uid', to=settings.AUTH_USER_MODEL, verbose_name='当前用户')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.category_article', verbose_name='分类'),
        ),
    ]
