from django.db import models
from squadup.settings import AUTH_USER_MODEL


class DefaultFields(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    creator = models.ManyToManyField(AUTH_USER_MODEL)