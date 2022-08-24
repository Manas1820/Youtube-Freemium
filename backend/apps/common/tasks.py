from __future__ import absolute_import

import os

from celery import shared_task

from backend.integrations.youtube_integration import YoutubeItegration


@shared_task
def yt_search(keyword):
    youtube_worker = YoutubeItegration()
    try:
        youtube_worker.search_keyword(keyword=keyword)
    except Exception as e:
        raise Exception('Failed to search keyword: %s' % keyword)
