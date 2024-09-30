import uuid

from django.db import models


class TimeStampModel(models.Model):
    """Provides auto-updating `created_at` and `updated_at` for models"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Provides UUID as a primary key for models"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
