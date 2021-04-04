from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    id = models.AutoField(primary_key=True)
    nikname = models.CharField(max_length=32)
    name = models.CharField(max_length=32, blank=True)
    surname = models.CharField(max_length=32, blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', null=False,
                                      default=0)
    email = models.EmailField(verbose_name='электронный адрес', unique=True)
    about = models.TextField(blank=True)
    company = models.CharField(max_length=32, blank=True)
