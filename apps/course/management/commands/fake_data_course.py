import random
import sys
import django
import faker

from django.utils import timezone
from django.test import TestCase
from apps.course.models import Courses,CourseList
from apps.user.models import *
from django.core.management.base import BaseCommand

# Create your tests here.
def fake_data_course():
    user=User.objects.all()
    categories=Courses.objects.all()
    fake=faker.Faker()


    for i in range(0,10):
        articles=CourseList.objects.create(
            titles=fake.word(),
            create_time=fake.date_time_between(
                start_date='-1y',end_date="now",
                tzinfo=timezone.get_current_timezone()
            ),
            #list_pic=fake.file_name(category="image",extension="png"),
            course=categories.order_by('?')[0],
            #desc=fake.sentence(nb_words=6,variable_nb_words=True),
            content='\n\n'.join(fake.paragraphs(10)),
        )
        articles.save()
        

    fake=faker.Faker('zh_CN')

    for i in range(0,10):
        ariticles=CourseList.objects.create(
            titles=fake.word(),
            create_time=fake.date_time_between(
                start_date='-1y',end_date="now",
                tzinfo=timezone.get_current_timezone()
            ),
            #list_pic=fake.file_name(category="image",extension="png"),
            course=categories.order_by('?')[0],
            #desc=fake.sentence(nb_words=6,variable_nb_words=True),
            content='\n\n'.join(fake.paragraphs(10)),
        )
        articles.save()
        

class Command(BaseCommand):
    help='Import init data for test'
    def handle(self,*args,**options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        fake_data_course()
        self.stdout.write(self.style.SUCCESS('end import'))