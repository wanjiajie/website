# Generated by Django 3.1.7 on 2021-04-27 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20190305_1423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courses',
            options={'ordering': ('-create_time',), 'verbose_name': '课程', 'verbose_name_plural': '课程'},
        ),
        migrations.RenameField(
            model_name='courselist',
            old_name='conent',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='courselist',
            old_name='add_time',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='courses',
            old_name='add_time',
            new_name='create_time',
        ),
    ]
