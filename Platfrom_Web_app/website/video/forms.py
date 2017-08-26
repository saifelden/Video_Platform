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
    title = forms.CharField(max_length=128,help_text="pleas enter the video title here")
    upload = forms.FileField()

    class Meta:
        model = Video
        exclude = ('user',)


