import os
import datetime
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from celery import shared_task
import yaml
import json

from .models import YT_videos

with open("config.yml", 'r') as ymlfile:
    config = yaml.full_load(ymlfile)

api_key_in_list = 0


@shared_task
def get_youtube_video():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    global api_key_in_list
    try:
        DEVELOPER_KEY = str(config['base']['api-key'][api_key_in_list])
    except IndexError:
        # Consumed all the keys and back to the
        # first key to try again if quota is replenished.
        api_key_in_list = 0
        reason = "All keys have their quota extinguished."
        return reason

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    time_to_get_videos_from = (
        datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    ).isoformat("T")+"Z"
    request = youtube.search().list(
        part="snippet",
        order="date",
        publishedAfter=time_to_get_videos_from,
        q="meme",
        type="video",
    )

    try:
        response = request.execute()
    except HttpError as err:
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get(
                'error').get('errors')[0].get('reason')
            if reason == "quotaExceeded" or reason == "dailyLimitExceeded":
                api_key_in_list += 1
                return reason
    else:
        save_youtube_video(response)
        return response


def save_youtube_video(request):
    for item in request['items']:
        video = YT_videos()
        video.videoId = item['id']['videoId']
        video.title = item['snippet']['title']
        video.description = item['snippet']['description']
        video.publishing_date = item['snippet']['publishedAt']
        video.default_thumbnail = str(
            item['snippet']['thumbnails']['default']['url'])
        video.medium_thumbnail = str(
            item['snippet']['thumbnails']['medium']['url'])
        video.high_thumbnail = str(
            item['snippet']['thumbnails']['high']['url'])
        video.save()
