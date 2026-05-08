import django_rq

from django.contrib import admin

from .models import Video
from .tasks import create_video_thumbnail


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "created_at")
    search_fields = ("title", "description", "category")
    list_filter = ("category", "created_at")
    readonly_fields = (
        "created_at",
        "hls_playlist",
        "hls_480p",
        "hls_720p",
        "hls_1080p",
    )

    def save_model(self, request, obj, form, change):
        """
        Saves the video and only regenerates the thumbnail
        when the thumbnail was removed in admin.
        """

        old_thumbnail = None

        if change:
            old_video = Video.objects.get(pk=obj.pk)
            old_thumbnail = old_video.thumbnail

        super().save_model(request, obj, form, change)

        if change and old_thumbnail and not obj.thumbnail:
            create_video_thumbnail(obj.id)