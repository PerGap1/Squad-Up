from django.db import models
from django.contrib.auth import get_user_model
from core.models import DefaultFields


class Game(DefaultFields): 
    artwork = models.ImageField()           # Mudar o nome?
    description = models.TextField()
    # developer = ?
    # genres = models.TextChoices()
    name = models.CharField(max_length=50)
    platforms = models.TextChoices()    # ?