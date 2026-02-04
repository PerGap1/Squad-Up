from django.db import models
from django.contrib.auth import get_user_model
from games.models import Game


class AbstractGroup(models.Model):
    '''
    # Pensando bem, não tenho certeza se o many to one funciona na direção que eu estou pensando...
    # será necessário checar a documentação

    banned_players = models.ManyToManyField(get_user_model())
    games = models.ManyToManyField(Game)
    host = models.ManyToOneRel(get_user_model())
    image = models.ImageField()                     # Não gostei do nome
    members = models.ManyToManyField(get_user_model())
    # chat...? Talvez criar um chat e fazer um relacionamento 1 pra 1
    name = models.CharField(max_length=50)
    privacy = models.TextChoices()                  # Público, privado e "linkado"
    # schedule: fazer um app pra isso
    # tag: criar um gerador de tags

    active = models.BooleanField()                  # Novamente este campo...provavelmente será uma boa extender models
    creator = models.ManyToOneRel(get_user_model())
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    '''
    pass


class Squad(AbstractGroup): pass
class Event(AbstractGroup): pass