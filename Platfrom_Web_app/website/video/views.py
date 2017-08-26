from django.shortcuts import render
from video.forms import UserForm , Video_Form
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from website.settings import MEDIA_ROOT
import os


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
def show_videos(request):
    return render(request,'video/show_videos.html',{})


@login_required
def add_video(request):
    form = Video_Form()

    if request.method == 'POST':
        form = Video_Form(request.POST)
        video = form.save(commit=False)
        video.user = User.id
        video.save()
        return show_videos(request)

    return render(request, 'video/add_video.html', {'form':form})


