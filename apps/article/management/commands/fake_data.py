import random
import sys
import django
import faker

from django.utils import timezone
from django.test import TestCase
from apps.article.models import *
from apps.user.models import *
from django.core.management.base import BaseCommand

# Create your tests here.
def fake_data():
    user=User.objects.all()
    categories=Category_Article.objects.all()
    fake=faker.Faker()


    for i in range(0,100):
        article=Article.objects.create(
            author=user[1],
            title=fake.word(),
            create_time=fake.date_time_between(
                start_date='-1y',end_date="now",
                tzinfo=timezone.get_current_timezone()
            ),
            list_pic=fake.file_name(category="image",extension="png"),
            category=categories.order_by('?')[0],
            keywords=fake.word(),
            desc=fake.sentence(nb_words=6,variable_nb_words=True),
            content='\n\n'.join(fake.paragraphs(10)),
        )
        article.save()
        

    fake=faker.Faker('zh_CN')

    for i in range(0,100):
        article=Article.objects.create(
            author=user[1],
            title=fake.word(),
            create_time=fake.date_time_between(
                start_date='-1y',end_date="now",
                tzinfo=timezone.get_current_timezone()
            ),
            list_pic=fake.file_name(category="image",extension="png"),
            category=categories.order_by('?')[0],
            keywords=fake.word(),
            desc=fake.sentence(nb_words=6,variable_nb_words=True),
            content='\n\n'.join(fake.paragraphs(10)),
        )
        article.save()
        

class Command(BaseCommand):
    help='Import init data for test'
    def handle(self,*args,**options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        fake_data()
        self.stdout.write(self.style.SUCCESS('end import'))