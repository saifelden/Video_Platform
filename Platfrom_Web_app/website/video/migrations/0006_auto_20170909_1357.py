# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-09 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import video.models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to=video.models.user_directory_path2),
        ),
    ]