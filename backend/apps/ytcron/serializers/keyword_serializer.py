from rest_framework import serializers

from backend.apps.ytcron.models import keyword


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = keyword
        fields = ["value", "id"]
        read_only_fields = []
