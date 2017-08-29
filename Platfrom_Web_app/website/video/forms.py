from django.contrib.auth.models import User
from django import forms
from video.models import Video
import os
from os.path import join



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class  Meta:
        model = User
        fields=('username','email','password')



class Video_Form (forms.ModelForm):
    upload = forms.FileField()
    class Meta:
        model = Video
        exclude=('user',)


class Youtube_Form (forms.Form):
    upload = forms.URLField()
