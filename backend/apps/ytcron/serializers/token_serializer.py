from rest_framework import serializers

from backend.apps.ytcron.models.token import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["id", "no_of_calls", "working"]
        read_only_fields = ["id", "no_of_calls", "working"]
