from django.db import models
from django.utils import timezone


class BaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now())
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    deleted = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name
