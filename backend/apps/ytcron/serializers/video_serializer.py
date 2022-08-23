from rest_framework import serializers

from backend.apps.ytcron.models.video import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
