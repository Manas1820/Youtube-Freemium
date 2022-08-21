import json

from django.db import models

# Create your models here.
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Keyword(models.Model):
    value = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super(Keyword, self).save(*args, **kwargs)
        schedule = IntervalSchedule.objects.create(
            every=10, period=IntervalSchedule.SECONDS
        )
        PeriodicTask.objects.create(
            name=f"Run Scheduler for keyword {self.value}",
            task="ytcron.tasks.search",
            interval=schedule,
            args=json.dumps([self.value]),
        )

    def __str__(self):
        return self.value
