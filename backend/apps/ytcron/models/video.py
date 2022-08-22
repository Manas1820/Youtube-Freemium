from django.db import models

# Considering  the list of important fields like
# Video title, description, publishing datetime, thumbnails URLs and any other fields you require


class Video(models.Model):
    _id = models.CharField(max_length=20, primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    thumbnail_default = models.URLField()
    channel_title = models.CharField(max_length=50)
    description = models.TextField()
    published_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["_id", "published_at"])]
        # descending order of published datetime.
        ordering = [
            "-published_at",
            "_id",
        ]
