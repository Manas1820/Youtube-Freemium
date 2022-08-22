from rest_framework import serializers

from backend.apps.ytcron.models import video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = [
            "_id",
            "kind",
            "title",
            "description",
            "thumbnail_default",
            "published_at",
            "channel_title",
        ]
