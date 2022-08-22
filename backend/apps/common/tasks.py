from __future__ import absolute_import

from celery import shared_task
import os
from backend.integrations.youtube_integration import YoutubeItegration


@shared_task
def yt_search(keyword):
    youtube_worker = YoutubeItegration()
    youtube_worker.search_keyword(keyword=keyword)
