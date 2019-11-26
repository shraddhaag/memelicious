from django.shortcuts import render
from .models import YT_videos
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def video_list(request):
    videos = YT_videos.objects.all().order_by('-publishing_date')
    page = request.GET.get('page', 1)
    
    paginator = Paginator(videos, 10)
    try:
        videos = paginator.page(page).object_list
    except PageNotAnInteger:
        videos = paginator.page(1).object_list
    except EmptyPage:
        videos = paginator.page(paginator.num_pages).object_list
    
    data = {"results": list(videos.values(
        "videoId",
        "title",
        "description",
        "publishing_date"
    ))}
    return JsonResponse(data)


