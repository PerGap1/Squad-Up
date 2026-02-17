from django.db import models
from squadup.settings import AUTH_USER_MODEL
from abc import abstractmethod

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

    @abstractmethod
    def create(**kwargs): pass

    @abstractmethod
    def delete(): pass