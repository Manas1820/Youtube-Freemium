from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import ModelAdmin

from backend.apps.ytcron.models import keyword, token, video, video_keyword


@admin.register(keyword.Keyword)
class KeywordAdmin(ModelAdmin):
    list_display = ("value",)


@admin.register(video.Video)
class VideoAdmin(ModelAdmin):
    list_display = (
        "_id",
        "title",
        "published_at",
    )
    list_filter = ("published_at",)
    search_fields = ("title",)


@admin.register(token.Token)
class TokenAdmin(ModelAdmin):
    list_display = (
        "token_value",
        "no_of_calls",
        "working",
    )
    list_filter = ("working",)

@admin.register(video_keyword.Video_Keyword)
class VideoKeywordAdmin(ModelAdmin):
    list_display = (
        "keyword",
        "video"
    )