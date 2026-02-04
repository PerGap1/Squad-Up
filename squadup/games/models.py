from django.db import models
from django.contrib.auth import get_user_model


class Game(models.Model): 
    '''
    active = models.BooleanField()          # É feito assim mesmo?
    artwork = models.ImageField()           # Mudar o nome?
    description = models.TextField()
    # developer = ?
    # genres = models.TextChoices()
    name = models.CharField(max_length=50)
    platforms = models.TextChoices()

    # Hidden fields
    # Alguma forma de setar o criador
    creator = models.ManyToManyField(get_user_model())
    # editable = False ?
    # Pensar nos melhores nomes para esses dois campos
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    '''
    pass