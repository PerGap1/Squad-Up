from django.db import models
from squadup.settings import AUTH_USER_MODEL

"""
Campos que estarão em todos os models, para facilitar com algumas informações que poderão ser usadas,
especialmente no desenvolvimento.

Está separado em campos padrão e campos padrão para coisas relacionadas a User, porque User ter um User creator gera diversos
problemas quanto a importações circulares. Isso acontece também com as tabelas intermediárias entre dois Users.
"""
class DefaultFieldsUserRelated(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class DefaultFields(DefaultFieldsUserRelated):
    class Meta:
        abstract = True

    creator = models.ManyToManyField(AUTH_USER_MODEL)