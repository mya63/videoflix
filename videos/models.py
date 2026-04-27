from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)

    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    hls_playlist = models.CharField(max_length=500, blank=True, null=True)
    hls_480p = models.CharField(max_length=500, blank=True, null=True)
    hls_720p = models.CharField(max_length=500, blank=True, null=True)
    hls_1080p = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title