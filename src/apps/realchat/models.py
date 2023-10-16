from django.db import models
from apps.core.models import GenericModel


class Chatrooms(GenericModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
