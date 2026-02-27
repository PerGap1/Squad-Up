from django.db import models
from squadup.settings import AUTH_USER_MODEL
from abc import abstractmethod
import datetime

"""
Campos que estarão em todos os models, para facilitar com algumas informações que poderão ser usadas,
especialmente no desenvolvimento.
"""
class DefaultFields(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    DEFAULT_FIELDS = []

    def is_modified(self):
        return self.modified > self.created + datetime.timedelta(minutes=2)

    @abstractmethod
    def create(**kwargs): ...
    # @abstractmethod
    # def list_attr(self): ...

    # @abstractmethod
    # def delete(): pass