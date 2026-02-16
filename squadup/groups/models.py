from django.db import models
from django.utils.translation import gettext_lazy as lazy

from abc import abstractmethod
from random import randint

from games.models import Game
from core.models import DefaultFields
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
    members = models.ManyToManyField(AUTH_USER_MODEL, through='Members')
    image = models.ImageField()

    games = models.ManyToManyField(Game)
    
    # chat...? Talvez importar um app chat, talvez criar nós mesmos e fazer um relacionamento 1 pra 1

    """
    Precisa ser sobrescrito, senão haverá colisão entre atributos related_name de Squads e Events
    """
    @property
    @abstractmethod
    def creator(self):
        return self.creator
    
    @property
    @abstractmethod
    def schedule(self):
        return self.schedule
    
    def __str__(self):
        return self.name

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


class Squad(AbstractGroup): # Talvez permitir que um grupo tenha subgrupos, tipo discord

    host = models.ForeignKey(AUTH_USER_MODEL, related_name='squad_host', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='squad_creator', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', related_name='squad_schedule', on_delete=models.CASCADE)

    @staticmethod
    def get_class():
        return 'Squad'


class Event(AbstractGroup):
    
    group = models.ForeignKey(Squad, blank=True, null=True, on_delete=models.CASCADE)  # Para que um grupo possa criar eventos de jogos
    
    host = models.ForeignKey(AUTH_USER_MODEL, related_name='event_host', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='event_creator', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', related_name='event_schedule', on_delete=models.CASCADE)

    @staticmethod
    def get_class():
        return 'Event'


class Members(DefaultFields):

    '''class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_1', 'user_2'], name='unique_constraint_friendship'
            )
        ]'''
    
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='member_user', on_delete=models.CASCADE)

    squad = models.ForeignKey(Squad, blank=True, null=True, related_name='member_squad', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, related_name='member_event', on_delete=models.CASCADE)

    @property
    def group(self):
        return self.squad or self.event
    
    @group.setter
    def group(self, obj):
        error_msg = "obj parameter must be an object of Squad or Event class"

        if not hasattr(obj, 'get_class'):
            raise ValueError(error_msg)
        
        if obj.get_class() == 'Squad':
            self.squad = obj
            self.event = None
        elif obj.get_class() == 'Event':
            self.event = obj
            self.squad = None
        else:
            raise ValueError(error_msg)
    

class Ban(DefaultFields):

    '''class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_1', 'user_2'], name='unique_constraint_friendship'
            )
        ]'''
    
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, related_name='ban_user', on_delete=models.CASCADE)

    squad = models.ForeignKey(Squad, blank=True, null=True, related_name='ban_squad', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, related_name='ban_event', on_delete=models.CASCADE)

    @property
    def group(self):
        return self.squad or self.event
    
    @group.setter
    def group(self, obj):
        error_msg = "obj parameter must be an object of Squad or Event class"

        if not hasattr(obj, 'get_class'):
            raise ValueError(error_msg)
        
        if obj.get_class() == 'Squad':
            self.squad = obj
            self.event = None
        elif obj.get_class() == 'Event':
            self.event = obj
            self.squad = None
        else:
            raise ValueError(error_msg)