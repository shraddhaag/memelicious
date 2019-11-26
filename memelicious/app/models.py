from django.db import models

class YT_videos(models.Model):

    videoId = models.CharField(max_length=30, primary_key=True, help_text="Unique video ID")
    title = models.CharField(max_length=100, help_text="Video title")
    description = models.CharField(max_length=255, help_text="Short description of the video")
    publishing_date = models.DateTimeField(help_text="Date and time when the video was published")
    default_thumbnail= models.URLField(help_text="Deault thumbnail URL")
    medium_thumbnail= models.URLField(help_text="Medium resolution thumbnail URL")
    high_thumbnail= models.URLField(help_text="High resolution thumbnail URL")

    class Meta:
        ordering = ['-publishing_date']
