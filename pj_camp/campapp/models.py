from django.db import models
from uuid import uuid4
from datetime import datetime

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    #uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, filename])


import os
from django.utils import timezone

def date_upload_to(instance, filename):
  # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
  ymd_path = timezone.now().strftime('%Y/%m/%d') 
  # 길이 32 인 uuid 값
  uuid_name = uuid4().hex
  # 확장자 추출
  extension = os.path.splitext(filename)[-1].lower()
  # 결합 후 return
  return '/'.join([
    ymd_path,
    uuid_name + extension,
  ])


class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField(null=False, unique=True)
    phone = models.TextField() 
    password1 = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    
class Notice(models.Model):
    writer = models.CharField(max_length=200)
    subject = models.TextField(null=True)
    content = models.TextField()
    count = models.IntegerField(default=0)
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    photo = models.ImageField(upload_to=date_upload_to, blank=True, null=True)
    top_fixed = models.BooleanField(default=False)
    rdate = models.DateTimeField()
    
class Board(models.Model):
    writer = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    hits = models.IntegerField(default=0)
    rdate = models.DateTimeField()
    
    

