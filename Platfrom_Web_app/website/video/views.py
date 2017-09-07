from django.shortcuts import render
from video.forms import UserForm, Video_Form, Youtube_Form
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Video
from django.contrib.auth.models import User
from website.settings import MEDIA_ROOT
from django.core.urlresolvers import reverse
import os
import sys
from pytube import YouTube

def index (request):
    return render(request,'video/index.html',{})

def about (request):
    return render(request,'video/about.html',{})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render (request , 'video/register.html', {'user_form':user_form , 'registered':registered })

def user_login (request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("your account is disabled")


        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'video/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def show_videos(request,user_id):
    user = User.objects.get(id=user_id)
    context_dict={'user':user}
    name=[]
    link=[]
    directory="/home/abdelrhman/Video_Platform/Platfrom_Web_app/website/media/user_{0}/".format(user.id)
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            name.append(filename)
            link.append('/media/user_{0}/{1}'.format(user.id,filename))
            continue
        else:
            continue
    list = zip(name, link)
    context_dict['list']=list
    return render(request,'video/show_videos.html',context_dict)


@login_required
def add_video(request,user_id):
    if request.method == 'POST':
        form = Video_Form(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user=User.objects.get(id=user_id)
            video.save()
            return HttpResponseRedirect('/video/')

    else:
        form = Video_Form()

    return render(request, 'video/add_video.html', {'form':form})

@login_required
def add_youtube_video(request,user_id):
    user=User.objects.get(id=user_id)
    if request.method == 'POST':
        form = Youtube_Form(request.POST)
        if form.is_valid():
            yt = YouTube(form.cleaned_data['upload'])
            video = yt.get('mp4','360p')
            video.download("/home/abdelrhman/Video_Platform/Platfrom_Web_app/website/media/user_{0}/".format(user_id))
            down_video=Video()
            x='x'
            for filename in os.listdir("/home/abdelrhman/Video_Platform/Platfrom_Web_app/website/media/user_{0}/".format(user_id)):
                x="/user_{0}/{1}".format(user_id,filename)
            down_video.upload=x
            down_video.user=User.objects.get(id=user_id)
            down_video.save()
            return HttpResponseRedirect('/video/')
    else:
        form = Youtube_Form()
    return render(request, 'video/add_youtube_video.html', {'form':form})
