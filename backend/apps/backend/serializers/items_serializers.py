from rest_framework import serializers

from backend.apps.backend.models import Item


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
        read_only_fields = ("id",)
