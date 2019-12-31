import uuid

from django.db import models


class User(models.Model):
    id: uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    friendly_name: str = models.CharField(max_length=30)
    slack_id: str = models.CharField(max_length=30, unique=True)
    splitwise_id: str = models.CharField(max_length=30, unique=True)
