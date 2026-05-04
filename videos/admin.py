from django.contrib import admin
from .models import Video


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