from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer
from .services import create_thumbnail, convert_to_hls
import os
from django.conf import settings


class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all().order_by("-created_at")
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        video = serializer.save()

        video_path = video.video_file.path

        # Thumbnail
        thumbnail_path = create_thumbnail(video_path)
        video.thumbnail = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT).replace("\\", "/")

        # HLS
        hls_path = convert_to_hls(video_path)
        print("HLS erstellt:", hls_path)


        video.hls_playlist = settings.MEDIA_URL + os.path.relpath(hls_path, settings.MEDIA_ROOT).replace("\\", "/")
        video.save()

        video.save()
    