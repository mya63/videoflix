import os

from django.conf import settings

from .models import Video
from .services import create_thumbnail, convert_to_hls


def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path

    thumbnail_path = create_thumbnail(video_path)
    video.thumbnail = os.path.relpath(
        thumbnail_path, settings.MEDIA_ROOT
    ).replace("\\", "/")

    hls_path = convert_to_hls(video_path)
    video.hls_playlist = settings.MEDIA_URL + os.path.relpath(
        hls_path, settings.MEDIA_ROOT
    ).replace("\\", "/")

    video.save()