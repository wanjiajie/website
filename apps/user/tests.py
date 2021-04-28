import random
import path
import sys
import datetime import delta
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

    def random_category():
        return random.choice(categories)

    def random_user():
        return random.choice(user)

    for i in range(0,100):
        article=Article.objects.create(
            'author'=random_user(),
            'title'=fake.paragraphs(),
            'create_time'=fake.data_time_between(
                start_data='-1y',end_data="now",
                tzinfo=timezone.get_current_timezone()
            )
            'category'=random_category(),
            'keywords'=random_category().name,
            'desc'=fake.paragraphs(),
            'content'='\n\n'.join(fake.paragraphs(10)),
        )
        article.save()
        

    fake=faker.Faker('zh_CN')

    for i in range(0,100):
        article=Article.objects.create(
            'author'=random_user(),
            'title'=fake.paragraphs(),
            'create_time'=fake.data_time_between(
                start_data='-1y',end_data="now",
                tzinfo=timezone.get_current_timezone()
            )
            'category'=random_category(),
            'keywords'=random_category().name,
            'desc'=fake.paragraphs(),
            'content'='\n\n'.join(fake.paragraphs(10)),
        )
        article.save()
        

class Command(BaseCommand):
    help='Import init data for test'
    def handle(self,*args,**options):
          self.stdout.write(self.style.SUCCESS('begin import'))
        fake_data()
        self.stdout.write(self.style.SUCCESS('end import'))