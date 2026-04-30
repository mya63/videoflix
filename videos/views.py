import os

import django_rq
from django.http import FileResponse, Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Video
from .serializers import VideoCreateSerializer, VideoListSerializer
from .tasks import process_video


class VideoListCreateView(generics.ListCreateAPIView):
    """
    Returns all videos or allows authenticated users to upload a new video.
    """

    queryset = Video.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Uses a create serializer for uploads and a list serializer for video lists.
        """

        if self.request.method == "POST":
            return VideoCreateSerializer

        return VideoListSerializer

    def perform_create(self, serializer):
        """
        Saves the uploaded video and starts background processing with RQ.
        """

        video = serializer.save()
        queue = django_rq.get_queue("default")
        queue.enqueue(process_video, video.id)


class HLSPlaylistView(APIView):
    """
    Serves the HLS playlist file for a specific video and resolution.
    """

    permission_classes = []

    def get(self, request, movie_id, resolution):
        """
        Returns the index.m3u8 playlist file if it exists.
        """

        video = generics.get_object_or_404(Video, id=movie_id)
        playlist_path = get_hls_file_path(video, resolution, "index.m3u8")

        if not os.path.exists(playlist_path):
            raise Http404("Playlist not found")

        return FileResponse(
            open(playlist_path, "rb"),
            content_type="application/vnd.apple.mpegurl",
        )


class HLSSegmentView(APIView):
    """
    Serves HLS transport stream segment files for video playback.
    """

    permission_classes = []

    def get(self, request, movie_id, resolution, segment):
        """
        Returns a .ts segment file for the requested video resolution.
        """

        video = generics.get_object_or_404(Video, id=movie_id)
        segment_path = get_hls_file_path(video, resolution, segment)

        if not os.path.exists(segment_path):
            raise Http404("Segment not found")

        return FileResponse(
            open(segment_path, "rb"),
            content_type="video/MP2T",
        )


def get_hls_file_path(video, resolution, filename):
    """
    Builds the absolute file path for an HLS playlist or segment file.
    """

    base_path = video.video_file.path
    base, _ = os.path.splitext(base_path)

    hls_dir = f"{base}_{resolution}_hls"

    if resolution not in ["480p", "720p", "1080p"]:
        raise Http404("Resolution not found")

    return os.path.join(hls_dir, filename)