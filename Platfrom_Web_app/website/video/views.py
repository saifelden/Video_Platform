from django.shortcuts import render
from video.forms import UserForm, Video_Form, Youtube_Form , UserEditForm , ProfileEditForm
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Video , Profile
from django.contrib.auth.models import User
from website.settings import MEDIA_ROOT
from django.core.urlresolvers import reverse
import os
import sys
from django.contrib import messages
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
            Profile.objects.create(limit=0,photo='/images/0.jpg',user=user)
            if not os.path.exists("/home/abdelrhman/programming/projects/Video_Platform/Platfrom_Web_app/website/media/user_{0}".format(user.id)):
                os.makedirs("/home/abdelrhman/programming/projects/Video_Platform/Platfrom_Web_app/website/media/user_{0}".format(user.id))
            registered=True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request , 'video/register.html', {'user_form':user_form , 'registered':registered })

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
    directory="/home/abdelrhman/programming/projects/Video_Platform/Platfrom_Web_app/website/media/user_{0}".format(user.id)
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
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = Video_Form(request.POST,request.FILES)
        #if (form.upload._size + user.profile.limit) > 5242880:
         #   return HttpResponse('memorylimitexceeded :D')
        if form.is_valid():
            video = form.save(commit=False)
            video.user=user
            video.save()
            return HttpResponseRedirect('/video/')
    else:
        form = Video_Form()

    return render(request, 'video/add_video.html', {'form':form})

@login_required
def add_youtube_video(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = Youtube_Form(request.POST)
        if form.is_valid():
            yt = YouTube(form.cleaned_data['upload'])
            video = yt.get('mp4','360p')
            video.download("/home/abdelrhman/programming/projects/Video_Platform/Platfrom_Web_app/website/media/user_{0}".format(user_id))
            down_video=Video()
            down_video.upload='/user_{0}/{1}.mp4'.format(user.id,video.filename)
            down_video.user=user
            down_video.save()
            return HttpResponseRedirect('/video/')
    else:
        form = Youtube_Form()
    return render(request, 'video/add_youtube_video.html', {'form':form})

@login_required
def myprofile (request,user_id):
    user = User.objects.get(id=user_id)
    return render(request,'video/myprofile.html',{'user':user,})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect('/video/')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'video/edit.html', {'user_form': user_form,'profile_form': profile_form})