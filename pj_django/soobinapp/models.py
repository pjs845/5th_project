# from django.db import models
from djongo import models

class Address(models.Model):
    name = models.CharField(max_length=200)
    addr = models.TextField()
    rdate = models.DateTimeField()
    
class Board(models.Model):
    b_name = models.CharField(max_length=210)
    b_email = models.TextField()
    b_title = models.CharField(max_length=300)
    b_content = models.CharField(max_length=1000)
    b_rdate = models.DateTimeField()

class Member(models.Model):
    m_name = models.CharField(max_length=200)
    m_email = models.TextField(null=False, unique=True)
    m_pwd = models.CharField(max_length=250)
    m_phone = models.CharField(max_length=100)
    m_rdate = models.DateTimeField()
    m_udate = models.DateTimeField()
    
class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    website = models.URLField()
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    salutation = models.CharField(max_length=100)
    email  = models.EmailField() 
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    publication_date = models.DateField()
    def __str__(self):
        return self.title



class User(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    publication_date = models.DateField()
    def __str__(self):
        return self.title