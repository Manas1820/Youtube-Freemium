from ast import keyword
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_psq import PsqMixin, Rule
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from backend.apps.common.custom_auto_schema import CustomAutoSchema
from backend.apps.common.pagination import DynamicPageSizePagination
from backend.apps.ytcron.models.keyword import Keyword
from backend.apps.ytcron.models.video import Video
from backend.apps.ytcron.serializers.keyword_serializer import (
    KeywordSerializer,
)
from backend.apps.ytcron.serializers.video_serializer import VideoSerializer
from backend.apps.ytcron.models.token import Token
from backend.apps.ytcron.serializers.token_serializer import TokenSerializer
from backend.integrations.youtube_integration import YoutubeItegration
from django.contrib.postgres.search import SearchVector


class VideosViewSet(
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    PsqMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    pagination_class = DynamicPageSizePagination
    filter_backends = (filters.DjangoFilterBackend,)
    http_method_names = ["get", "patch", "post"]
    swagger_schema = CustomAutoSchema
    permission_classes = [IsAuthenticated]
    psq_rules = {
        "create": [Rule([IsAuthenticated], VideoSerializer)],
        "partial_update": [Rule([IsAuthenticated], VideoSerializer)],
        "list": [Rule([IsAuthenticated], VideoSerializer)],
        "update": [Rule([IsAuthenticated], VideoSerializer)],
        "search": [Rule([IsAuthenticated], VideoSerializer)],
        "add": [Rule([IsAuthenticated], KeywordSerializer)],
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        return Video.objects.all().order_by("-published_at")

    # def list(self,request, *args, **kwargs):
    #     return Video.objects.annotate( search=SearchVector('title', 'description')).filter(search="").order_by(
    #         "-published_at"
    #     )

    @action(methods=["post"], detail=False, serializer_class=KeywordSerializer)
    def add(self, request):
        user = self.request.user
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        queryset = serializer.data.get("value")
        try:
            yt = YoutubeItegration()
            keyword = Keyword.objects.get_or_create(value=queryset.lower())[0]
            yt.search_keyword(keyword.value)
            user.keyword = keyword
            user.save()
        except Exception as e:
            raise ValidationError({"detail": "Tokens Not Found"})
        return Response(
            {"message": "Keyword Added To History"}, status=status.HTTP_200_OK
        )

    @action(methods=["post"], detail=False, serializer_class=VideoSerializer)
    def search(self, request):
        serializer = KeywordSerializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        queryset = serializer.data.get("value")
        try:

            serializer = (
                Video.objects.annotate(search=SearchVector("title", "description"))
                .filter(search=queryset)
                .order_by("-published_at")
            )

            page = self.paginate_queryset(serializer)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(serializer, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError({"detail": str(e)})
