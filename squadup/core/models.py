from django.db import models
from django.contrib.auth import get_user_model


class DefaultFields:
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    creator = models.ManyToManyField(get_user_model())