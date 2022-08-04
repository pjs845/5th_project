from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField(null=False, unique=True)
    phone = models.TextField() 
    password1 = models.TextField()
    rdate = models.TextField()
    udate = models.DateTimeField()