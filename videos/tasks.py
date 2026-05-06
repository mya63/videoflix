import os

from django.conf import settings

from .models import Video

from .services import create_thumbnail, convert_to_hls


def get_media_path(file_path):
    """
    Converts an absolute media file path into a public media URL.
    """

    return settings.MEDIA_URL + os.path.relpath(
        file_path, settings.MEDIA_ROOT
    ).replace("\\", "/")


def process_video(video_id):
    """
    Creates a thumbnail, converts the video to HLS and updates generated file paths.
    """

    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path

    thumbnail_path = create_thumbnail(video_path)
    hls_paths = convert_to_hls(video_path)

    thumbnail = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT).replace("\\", "/")

    Video.objects.filter(id=video_id).update(
        thumbnail=thumbnail,
        hls_480p=get_media_path(hls_paths["480p"]),
        hls_720p=get_media_path(hls_paths["720p"]),
        hls_1080p=get_media_path(hls_paths["1080p"]),
        hls_playlist=get_media_path(hls_paths["720p"]),
    )