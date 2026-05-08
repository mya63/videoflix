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
    Converts the video to HLS and only creates a thumbnail
    if no custom thumbnail was uploaded.
    """

    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path

    if video.thumbnail:
        thumbnail = video.thumbnail.name
    else:
        thumbnail_path = create_thumbnail(video_path)
        thumbnail = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT).replace("\\", "/")

    hls_paths = convert_to_hls(video_path)

    Video.objects.filter(id=video_id).update(
        thumbnail=thumbnail,
        hls_480p=get_media_path(hls_paths["480p"]),
        #hls_720p=get_media_path(hls_paths["720p"]),
        #hls_1080p=get_media_path(hls_paths["1080p"]),
        #hls_playlist=get_media_path(hls_paths["720p"]),
    )
        
def create_video_thumbnail(video_id):
    """
    Creates only a new thumbnail without converting the video again.
    """

    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path

    thumbnail_path = create_thumbnail(video_path)
    thumbnail = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT).replace("\\", "/")

    Video.objects.filter(id=video_id).update(thumbnail=thumbnail)