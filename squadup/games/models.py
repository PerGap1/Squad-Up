from django.db import models
from core.models import DefaultFields

from squadup.settings import AUTH_USER_MODEL


class Game(DefaultFields): 
    name = models.CharField(max_length=50)
    artwork = models.ImageField()           # Mudar o nome?
    description = models.TextField()
    # developer = ?
    # genres = models.TextChoices()         # Dá para buscar com api da steam
    released = models.DateField()
    # platforms = models.TextChoices()    # Acho que dá para cancelar, nem a Steam mostra muito sobre plataformas

    creator = models.ManyToManyField(AUTH_USER_MODEL, related_name='game_creator')