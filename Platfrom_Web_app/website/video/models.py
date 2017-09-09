import os
from django.db import models
from django.contrib.auth.models import User
from os.path import join


def user_directory_path(instance, title):
    return 'user_{0}/{1}'.format(instance.user.id, title)

def user_directory_path2(instance, title):
    return 'images/user_{0}/{1}'.format(instance.user.id,title)


class Video(models.Model):
    user = models.ForeignKey(User)
    upload = models.FileField(upload_to=user_directory_path)


class Profile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to=user_directory_path2,blank=True)
    limit = models.FloatField(default=0)