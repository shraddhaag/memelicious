import os
import datetime
import googleapiclient.discovery
from celery import shared_task
from django.http import JsonResponse
import yaml

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
    DEVELOPER_KEY = config['api-key']

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    time_to_get_videos_from = (datetime.datetime.utcnow()-datetime.timedelta(minutes=1)).isoformat("T")+"Z"

    request = youtube.search().list(
        part="snippet",
        order="date",
        publishedAfter=time_to_get_videos_from,
        q="memes",
        type="video"
    )
    response = request.execute()

    return response