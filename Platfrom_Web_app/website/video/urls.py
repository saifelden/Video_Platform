from django.conf.urls import url
from video import views

urlpatterns =[
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^show_videos/$',views.show_videos,name='show_videos'),
    url(r'^add_video/$',views.add_video,name='add_video'),

]
