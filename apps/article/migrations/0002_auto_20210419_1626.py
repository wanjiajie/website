# Generated by Django 3.1.7 on 2021-04-19 16:26

import apps.article.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='list_pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=apps.article.models.article_directory_path, verbose_name='列表图'),
        ),
    ]
