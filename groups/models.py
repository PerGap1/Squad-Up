from django.db import models
from django.utils.translation import gettext_lazy as lazy

from abc import abstractmethod
from random import randint

from games.models import Game
from core.models import DefaultFields
from squadup.settings import AUTH_USER_MODEL
from schedule.models import Schedule


# Unificar o que der em um superior, e chamar o criador de tag
class SquadManager(models.Manager):

    def create_schedule(squad):
        if not squad.schedule:
            squad.schedule = Schedule.objects.create(holder=squad)

    def create(self, *args, **kwargs):
        squad = super().create(*args, **kwargs)
        SquadManager.create_schedule(squad)
        return squad
    
    def acreate(self, *args, **kwargs):
        squad = super().acreate(*args, **kwargs)
        SquadManager.create_schedule(squad)
        return squad
    

class EventManager(models.Manager):

    def create_schedule(event):
        if not event.schedule:
            event.schedule = Schedule.objects.create(holder=event)

    def create(self, *args, **kwargs):
        event = super().create(*args, **kwargs)
        EventManager.create_schedule(event)
        return event
    
    def acreate(self, *args, **kwargs):
        event = super().acreate(*args, **kwargs)
        EventManager.create_schedule(event)
        return event
    

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
    image = models.ImageField()

    members = models.ManyToManyField(AUTH_USER_MODEL, through='Members')
    games = models.ManyToManyField(Game)
    
    # chat...? Talvez importar um app chat, talvez criar nós mesmos e fazer um relacionamento 1 pra 1

    def __str__(self):
        return self.name

    def create_tag(self): 
        valid_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        tag = ''
        for _ in range(7):
            tag += valid_characters[randint(0, len(valid_characters))]
        return tag


class Squad(AbstractGroup): # Talvez permitir que um grupo tenha subgrupos, tipo discord

    host = models.ForeignKey(AUTH_USER_MODEL, null=True, related_name='squad_host', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, null=True, related_name='squad_creator', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='squad_schedule', on_delete=models.CASCADE)

    objects = SquadManager()

    @staticmethod
    def get_class():
        return 'Squad'


class Event(AbstractGroup):
    
    group = models.ForeignKey(Squad, blank=True, null=True, on_delete=models.CASCADE)  # Para que um grupo possa criar eventos de jogos
    
    host = models.ForeignKey(AUTH_USER_MODEL, null=True, related_name='event_host', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, null=True, related_name='event_creator', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='event_schedule', on_delete=models.CASCADE)

    objects = EventManager()

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