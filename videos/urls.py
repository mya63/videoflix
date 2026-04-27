from django.urls import path
from .views import VideoListCreateView, HLSPlaylistView, HLSSegmentView

urlpatterns = [
    path("video/", VideoListCreateView.as_view(), name="video-list-create"),
    path(
        "video/<int:movie_id>/<str:resolution>/index.m3u8",
        HLSPlaylistView.as_view(),
        name="hls-playlist",
    ),
    path(
        "video/<int:movie_id>/<str:resolution>/<str:segment>/",
        HLSSegmentView.as_view(),
        name="hls-segment",
    ),
]