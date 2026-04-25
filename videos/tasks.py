import os

from django.conf import settings

from .models import Video
from .services import create_thumbnail, convert_to_hls


def get_media_path(file_path):
    return settings.MEDIA_URL + os.path.relpath(
        file_path, settings.MEDIA_ROOT
    ).replace("\\", "/")


def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path

    thumbnail_path = create_thumbnail(video_path)
    hls_paths = convert_to_hls(video_path)

    video.thumbnail = os.path.relpath(
        thumbnail_path, settings.MEDIA_ROOT
    ).replace("\\", "/")
    video.hls_480p = get_media_path(hls_paths["480p"])
    video.hls_720p = get_media_path(hls_paths["720p"])
    video.hls_1080p = get_media_path(hls_paths["1080p"])
    video.hls_playlist = video.hls_720p

    video.save()