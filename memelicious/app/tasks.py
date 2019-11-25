from celery import shared_task

@shared_task
def get_videos(x,y):
    return x+y