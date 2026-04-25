from django.urls import path
from .views import VideoListCreateView

urlpatterns = [
    path("videos/", VideoListCreateView.as_view(), name="video-list-create"),
]