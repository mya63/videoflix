import django_rq
from rest_framework import generics

from .models import Video
from .serializers import VideoSerializer
from .tasks import process_video


class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all().order_by("-created_at")
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        video = serializer.save()
        queue = django_rq.get_queue("default")
        queue.enqueue(process_video, video.id)