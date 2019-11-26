import os
import datetime
import googleapiclient.discovery
from celery import shared_task
from django.http import JsonResponse
import yaml

from .models import YT_videos

with open("config.yml", 'r') as ymlfile:	
    config = yaml.full_load(ymlfile)

@shared_task
def get_videos(x,y):
    return x+y
@shared_task
def get_youtube_video():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = str(config['base']['api-key'])

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    time_to_get_videos_from = (datetime.datetime.utcnow()-datetime.timedelta(minutes=1)).isoformat("T")+"Z"

    request = youtube.search().list(
        part="snippet",
        order="date",
        publishedAfter=time_to_get_videos_from,
        q="comedy",
        type="video"
    )
    response = request.execute()
    save_youtube_video(response)
    return response['items'][0]['snippet']['thumbnails']['default']['url']

def save_youtube_video(request):
        for item in request['items']:
            video = YT_videos()
            video.videoId = item['id']['videoId']
            video.title = item['snippet']['title']
            video.description = item['snippet']['description']
            video.publishing_date = item['snippet']['publishedAt']
            video.default_thumnail = str(item['snippet']['thumbnails']['default']['url'])
            video.medium_thumnail = str(item['snippet']['thumbnails']['medium']['url'])
            video.high_thumnail =  str(item['snippet']['thumbnails']['high']['url'])
            video.save()

