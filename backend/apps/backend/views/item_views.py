from drf_psq import PsqMixin, Rule
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from backend.apps.backend.models import Item
from backend.apps.backend.serializers import (
    ItemsSerializer,
)


class ItemsViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    PsqMixin,
    GenericViewSet,
):
    http_method_names = ["patch", "post", "get", "delete"]
    pagination_class = None
    permission_classes = [AllowAny]
    psq_rules = {
        "list": [Rule([AllowAny], ItemsSerializer)],
        "retrieve": [Rule([AllowAny], ItemsSerializer)],
        "create": [Rule([AllowAny], ItemsSerializer)],
        "partial_update": [Rule([AllowAny], ItemsSerializer)],
        "destroy": [Rule([AllowAny], ItemsSerializer)],
    }

    def get_queryset(self):
        return Item.objects.all()
