#!/usr/bin/env python
#-*-coding:utf-8-*-
import datetime
import os
import smtplib
from email.header import make_header
from email.message import EmailMessage

from email.mime.application import MIMEApplication

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import EmailMultiAlternatives
from django.test import TestCase

#from apps.article.models import Article



# Create your tests here.





