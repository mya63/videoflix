from django.db import models


class Video(models.Model):
    """
    Stores uploaded videos and generated HLS file references.
    """

    CATEGORY_CHOICES = [
        ("nature", "Nature"),
        ("education", "Education"),
        ("entertainment", "Entertainment"),
        ("sports", "Sports"),
        ("documentary", "Documentary"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="entertainment",
    )

    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    hls_playlist = models.CharField(max_length=500, blank=True, null=True)
    hls_480p = models.CharField(max_length=500, blank=True, null=True)
    hls_720p = models.CharField(max_length=500, blank=True, null=True)
    hls_1080p = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        """
        Returns the video title as the readable model representation.
        """

        return self.title