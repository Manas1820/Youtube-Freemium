from rest_framework import serializers

from backend.apps.ytcron.models import token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = token
        fields = ["id", "no_of_calls", "working"]
        read_only_fields = ["id", "no_of_calls", "working"]
