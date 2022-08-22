from django.db import models

from backend.apps.ytcron.models.keyword import Keyword
from backend.apps.ytcron.models.video import Video


class Video_Keyword(models.Model):
    keyword = models.ForeignKey(
        Keyword, on_delete=models.CASCADE, related_name="related_videos"
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="related_keywords"
    )

    class Meta:
        unique_together = ["keyword", "video"]
