from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class UserType(models.Model):
    type_name = models.CharField(max_length=255)


class User(AbstractUser, models.Model):
    pass


class Topic(models.Model):
    level = models.CharField(max_length=255)
    voted_for = models.BooleanField()
    available = models.BooleanField()
    checked = models.BooleanField()


class Faculty(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=255)


class Review(models.Model):
    is_finished = models.BooleanField
    finished_date = models.DateTimeField(default=timezone.now)

class Thesis():
    pass


class Defense():
    pass
