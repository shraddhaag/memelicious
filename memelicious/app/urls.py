from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.video_list, name='video-list')
]