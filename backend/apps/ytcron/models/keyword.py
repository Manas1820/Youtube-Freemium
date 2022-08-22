import json

from django.db import models
from django_celery_beat.models import IntervalSchedule, PeriodicTask

class Keyword(models.Model):
    value = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        schedule = IntervalSchedule.objects.create(
            every=10, period=IntervalSchedule.SECONDS
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name=f'Keyword Scheduler {self.value}',
            task='backend.apps.common.tasks.yt_search',
            args=json.dumps([self.value])
        )
        super(Keyword, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.value
