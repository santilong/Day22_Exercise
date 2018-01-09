from django.db import models

# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=32)

class hosts(models.Model):
    hostname = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(max_length=32,unique=True)
    port = models.IntegerField()
