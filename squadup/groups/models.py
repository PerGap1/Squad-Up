from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as lazy

from abc import abstractmethod
from random import randint

from games.models import Game
from core.models import DefaultFields, DefaultFieldsUserRelated
from squadup.settings import AUTH_USER_MODEL


class AbstractGroup(DefaultFields):
    class Meta:
        abstract = True
    
    class Privacy(models.TextChoices):
        PUBLIC = 'PB', lazy('Public')
        LINKED = 'LK', lazy('Linked')
        PRIVATE = 'PR', lazy('Private')

    name = models.CharField(max_length=50)
    privacy = models.CharField(max_length=2, choices=Privacy, default=Privacy.PUBLIC)
    tag = models.CharField(max_length=7, unique=True, editable=False)     # Ainda não consigo acessar coisas dentro da classe...
    members = models.ManyToManyField(AUTH_USER_MODEL)
    image = models.ImageField()

    games = models.ManyToManyField(Game)
    
    # chat...? Talvez importar um app chat, talvez criar nós mesmos e fazer um relacionamento 1 pra 1
    # schedule: fazer um app pra isso

    """
    Precisa ser sobrescrito, senão haverá colisão entre atributos related_name de Squads e Events
    """
    @property
    @abstractmethod
    def creator(self):
        return self.creator

    def create_tag(self): 
        valid_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        tag = ''
        for _ in range(7):
            tag += valid_characters[randint(0, len(valid_characters))]
        return tag
    
    @classmethod
    def create(cls, name, privacy, members, image, games, host):
        book = cls(name, privacy, members, image, games, host)
        book.tag = cls.create_tag()
        return book


class Ban(DefaultFieldsUserRelated):
    '''
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"], name="unique_constraint_friendship"
            )
        ]

    # Acho que por ser AbstractGroup, pode dar erro
    group = models.ForeignKey(AbstractGroup, related_name='ban_group', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='ban_user', on_delete=models.CASCADE)
    '''
    pass


class Squad(AbstractGroup): # Talvez permitir que um grupo tenha subgrupos, tipo discord
    host = models.ForeignKey(get_user_model(), related_name='squad_host', on_delete=models.CASCADE)
    creator = models.ManyToManyField(AUTH_USER_MODEL, related_name='squad_creator')


class Event(AbstractGroup):
    '''
    group = models.ForeignKey(Squad, blank=True, on_delete=models.CASCADE)  # Para que um grupo possa criar eventos de jogos
    '''
    host = models.ForeignKey(get_user_model(), related_name='event_host', on_delete=models.CASCADE)
    creator = models.ManyToManyField(AUTH_USER_MODEL, related_name='event_creator')