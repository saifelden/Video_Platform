import os
from django.db import models
from django.contrib.auth.models import User
from os.path import join

def user_directory_path(instance, title):
    return 'user_{0}/{1}'.format(instance.user.id, title)


class Video(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    upload = models.FileField(upload_to=user_directory_path)

    def get_videos_path(self):
        mypath={}
        for root, dirs, files in os.walk('website/media/user_{0}'.format(User.id)):
                mypath += os.sep.join(os.path.join(root, files).split(os.sep)[4:])

        return mypath
