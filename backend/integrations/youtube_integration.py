from signal import valid_signals

import googleapiclient.discovery
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied, ValidationError

from backend.apps.ytcron.models import video_keyword
from backend.apps.ytcron.models.keyword import Keyword
from backend.apps.ytcron.models.token import Token
from backend.apps.ytcron.models.video import Video


class YoutubeItegration:
    def __init__(self):
        self.token = self.fetch_token()

        # reference - https://developers.google.com/youtube/v3/code_samples/code_snippets?apix_params=%7B%22part%22%3A%5B%22manas%22%5D%2C%22maxResults%22%3A25%7D&apix=true
        try:
            self.service = googleapiclient.discovery.build(
                "youtube",
                "v3",
                developerKey=self.token.token_value,
            )
        except Exception as e:
            self.token.working = False
            self.token.save()
            raise PermissionDenied({"detail": "Tokens Exausted"})

    def fetch_token(self):
        curr_token = Token.objects.filter().first()
        if not curr_token:
            raise PermissionDenied({"detail": "Tokens Exausted"})

        # A read operation that retrieves a list of resources -- channels, videos, playlists -- usually costs 1 unit.
        # A write operation that creates, updates, or deletes a resource usually has costs 50 units.
        # A search request costs 100 units.
        # A video upload costs 1600 units.

        curr_token.no_of_calls += 1
        curr_token.save()
        if curr_token.no_of_calls >= 100:
            curr_token.working = False
            curr_token.save()

        return Token.objects.filter(working=True).first()

    def search_keyword(self, keyword):
        request = self.service.search().list(
            q=keyword,
            part="snippet",
            type="video",
            maxResults=10,
            publishedAfter="2022-04-01T00:00:00Z",
            order="relevance",
        )

        try:
            response = request.execute()
        except Exception as e:
            self.token.working = False
            self.token.save()
            raise PermissionDenied({"detail": "Tokens Exausted"})

        # Sample response
        #  {
        #   "kind": "youtube#searchResult",
        #   "etag": etag,
        #   "id": {
        #     "kind": string,
        #     "videoId": string,
        #     "channelId": string,
        #     "playlistId": string
        #   },
        #   "snippet": {
        #     "publishedAt": datetime,
        #     "channelId": string,
        #     "title": string,
        #     "description": string,
        #     "thumbnails": {
        #       (key): {
        #         "url": string,
        #         "width": unsigned integer,
        #         "height": unsigned integer
        #       }
        #     },
        #     "channelTitle": string,
        #     "liveBroadcastContent": string
        #   }
        # }

        for item in response["items"]:
            try:
                video = Video.objects.get_or_create(
                    _id=item["id"]["videoId"],
                    kind=item["id"]["kind"],
                    channel_title=item["snippet"]["channelTitle"],
                    title=item["snippet"]["title"],
                    description=item["snippet"]["description"],
                    published_at=item["snippet"]["publishedAt"],
                    thumbnail_default=item["snippet"]["thumbnails"]["default"]["url"],
                )
                curr_keyword = Keyword.objects.get(value=keyword)

                link = video_keyword.Video_Keyword.objects.create(
                    keyword=curr_keyword, video=video[0]
                )
                link.save()
            except IntegrityError:
                pass
            except Exception as e:
                raise ValidationError({"error": "Error searching the keyword"})
        return
