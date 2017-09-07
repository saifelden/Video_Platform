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
    upload = forms.URLField(max_length=1000)
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url']=url
            return cleaned_data


    class Meta:
        fields=('upload',)


