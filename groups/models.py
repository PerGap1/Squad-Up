from django.db import models
from django.utils.translation import gettext_lazy as lazy

from random import randint

from games.models import Game
from core.models import DefaultFields
from squadup.settings import AUTH_USER_MODEL
from schedule.models import Schedule

# Chamar o criador de tag
class GroupManager(models.Manager):

    @staticmethod
    def tag_creator():      # É possível cair com uma tag obscena ou algo do tipo
        # Talvez dê para pensar em uma forma melhor, sem recursão
        valid_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        tag = ''
        for _ in range(7):
            tag += valid_characters[randint(0, len(valid_characters) - 1)]

        if Squad.objects.filter(tag=tag) or Event.objects.filter(tag=tag):
            return GroupManager.tag_creator()
        return tag

    def create(self, *args, **kwargs):
        group = super().create(tag=GroupManager.tag_creator(), *args, **kwargs)
        GroupManager._create_schedule(group)
        return group
    
    def acreate(self, *args, **kwargs):
        group = super().acreate(tag=GroupManager.tag_creator(), *args, **kwargs)
        GroupManager._create_schedule(group)
        return group
    
    @staticmethod
    def _create_schedule(group):
        if not group.schedule:
            group.schedule = Schedule.objects.create(holder=group)


class AbstractGroup(DefaultFields):
    class Meta:
        abstract = True
    
    class Privacy(models.TextChoices):
        PUBLIC = 'PB', lazy('Public')
        LINKED = 'LK', lazy('Linked')
        PRIVATE = 'PR', lazy('Private')

    name = models.CharField(max_length=50, null=False, blank=False)     # Unique?
    privacy = models.CharField(max_length=2, choices=Privacy, default=Privacy.PUBLIC, blank=False)
    tag = models.CharField(max_length=7, unique=True, editable=False, null=False, blank=False)
    image = models.ImageField()

    members = models.ManyToManyField(AUTH_USER_MODEL, through='Members')
    games = models.ManyToManyField(Game)

    objects = GroupManager()
    
    # chat...? Talvez importar um app chat, talvez criar nós mesmos e fazer um relacionamento 1 pra 1

    def __str__(self):
        return self.name


class Squad(AbstractGroup): # Talvez permitir que um grupo tenha subgrupos, tipo discord

    # Talvez trocar o valor de null dos dois próximos para False
    host = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, related_name='squad_host', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, related_name='squad_creator', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='squad_schedule', on_delete=models.CASCADE)

    @staticmethod
    def get_class():
        return 'Squad'


class Event(AbstractGroup):
    
    group = models.ForeignKey(Squad, blank=True, null=True, on_delete=models.CASCADE)  # Para que um grupo possa criar eventos de jogos
    
    # Talvez trocar o valor de null dos dois próximos para False
    host = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, related_name='event_host', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, related_name='event_creator', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='event_schedule', on_delete=models.CASCADE)

    @staticmethod
    def get_class():
        return 'Event'

# Talvez juntar a propriedade de group das duas próximas tabelas em uma só
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