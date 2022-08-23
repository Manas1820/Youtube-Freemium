from rest_framework import serializers

from backend.apps.ytcron.models.keyword import Keyword


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"
