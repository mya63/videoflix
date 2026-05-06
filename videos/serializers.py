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
        Returns the thumbnail URL or a fallback if no thumbnail exists.
        """

        request = self.context.get("request")

        if obj.thumbnail:
            url = obj.thumbnail.url
        else:
            url = "/media/videos/default_thumbnail.jpg"

        if request:
            return request.build_absolute_uri(url)

        return url


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