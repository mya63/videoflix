from rest_framework import serializers

from .models import Video


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializes video data for listing videos in the frontend.
    """

    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "created_at",
            "title",
            "description",
            "thumbnail_url",
            "category",
        ]

    def get_thumbnail_url(self, obj):
        """
        Returns the absolute thumbnail URL if a request context is available.
        """

        request = self.context.get("request")

        if not obj.thumbnail:
            return None

        if request:
            return request.build_absolute_uri(obj.thumbnail.url)

        return obj.thumbnail.url


class VideoCreateSerializer(serializers.ModelSerializer):
    """
    Serializes uploaded video data for creating new video entries.
    """

    class Meta:
        model = Video
        fields = [
            "title",
            "description",
            "category",
            "video_file",
        ]