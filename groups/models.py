from django.db import models
from django.utils.translation import gettext_lazy as lazy

from abc import abstractmethod
from random import randint

from games.models import Game
from core.models import DefaultFields
from squadup.settings import AUTH_USER_MODEL
from schedule.models import Schedule
from django.contrib.auth import get_user_model


class AbstractGroup(DefaultFields):
    class Meta:
        abstract = True
    
    class Privacy(models.TextChoices):
        PUBLIC = 'PB', lazy('Public')
        LINKED = 'LK', lazy('Linked')
        PRIVATE = 'PR', lazy('Private')

    class ErrorMessages:
        ERROR_ADDING      = "Coudn't add %s to group %s: already in there"
        ERROR_REMOVING    = "Coudn't remove %s from group's %s: not in there"
        ERROR_PROMOTING   = "Coudn't promote %s to host: already the host"
        ERROR_BANNING     = "Cannot ban user %s: already banned"
        ERROR_DELETING    = "Coudn't delete group %s: already deleted"
        SINGLE_TYPE_ERROR = "Object of %s type expected, got %s instead"

    name = models.CharField(max_length=50)
    privacy = models.CharField(max_length=2, choices=Privacy, default=Privacy.PUBLIC)
    tag = models.CharField(max_length=7, unique=True, editable=False)
    image = models.ImageField(default='default_pfp.jpg', upload_to='profile_pics')

    games = models.ManyToManyField(Game)

    creator = ...
    host = ...
    members = ...
    banned_users = ...
    schedule = ...

    REQUIRED_FIELDS = ['name', 'creator', 'host']
    
    # chat...? Talvez importar um app chat, talvez criar nós mesmos e fazer um relacionamento 1 pra 1
    
    @staticmethod
    def tag_creator():
        valid_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        tag = ''
        for _ in range(7):
            tag += valid_characters[randint(0, len(valid_characters) - 1)]

        if Squad.objects.filter(tag=tag) or Event.objects.filter(tag=tag):
            return AbstractGroup.tag_creator()
        return tag
    
    def delete(self, *args, **kwargs):
        if not self.active:
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_DELETING % self.name)
        self.active = False

    """Related to host"""
    def promote_to_host(self, user):
        if self.host is user:
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_PROMOTING % (user.username))
        self.host = user
    
    """Related to members and games"""
    def add(self, object):
        obj_type = type(object)

        if obj_type is get_user_model():
            AbstractGroup._add_user(object)
        elif obj_type is Game:
            AbstractGroup._add_game(object)
        else:
            raise TypeError(f"Object of User or Game type expected, got {obj_type} instead")
        
    def add_many(self, objects):
        for object in objects:
            AbstractGroup.add(object)

    def remove(self, object):
        obj_type = type(object)

        if obj_type is get_user_model():
            AbstractGroup._remove_user(object)
        elif obj_type is Game:
            AbstractGroup._remove_game(object)
        else:
            raise TypeError(f"Object of User or Game type expected, got {obj_type} instead")

    def remove_many(self, objects):
        for object in objects:
            AbstractGroup.remove(object)

    def ban(self, user): 
        AbstractGroup._ban(user)

    def ban_many(self, users):
        for user in users:
            AbstractGroup._ban(user)   
        
    """Private functions"""
    def _add_user(self, user):
        if user in self.members:
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_ADDING % (user.username, 'members'))
        if not type(user) is get_user_model():
            raise TypeError(AbstractGroup.ErrorMessages.SINGLE_TYPE_ERROR % ('User', type(user)))
        
        self.members.add(user)

    def _remove_user(self, user):
        if not user in self.members.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_REMOVING % (user.username, 'members'))
        if not type(user) is get_user_model():
            raise TypeError(AbstractGroup.ErrorMessages.SINGLE_TYPE_ERROR % ('User', type(user)))
        
        self.members.remove(user)

    def _ban(self, user):
        AbstractGroup._remove_user(user)

        if user in self.banned_users.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_BANNING % user.username)
        self.banned_users.add(user)

    def _add_game(self, game): 
        if game in self.games.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_ADDING % (game.name, 'games'))
        if not type(game) is Game:
            raise TypeError(AbstractGroup.ErrorMessages.SINGLE_TYPE_ERROR % ('Game', type(game)))
        
        self.games.add(game)

    def _remove_game(self, game):
        if not game in self.games.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_REMOVING % (game.name, 'games'))
        if not type(game) is Game:
            raise TypeError(AbstractGroup.ErrorMessages.SINGLE_TYPE_ERROR % ('Game', type(game)))
        
        self.games.remove(game)

    def _validate(cls, **kwargs):        
        not_given = []
        for field in cls.REQUIRED_FIELDS:
            if not kwargs.get(field):
                not_given.append(field)

        if not_given:
            raise ValueError(f"Some required field(s) were not passed: {', '.join(not_given)}")

    """Dunder methods"""
    def __str__(self):
        return self.name
    
    def __len__(self):
        return len(self.members.all())
    
    """Abstract methods"""
    @abstractmethod
    def create(self): ...


class Squad(AbstractGroup): # Talvez permitir que um grupo tenha subgrupos, tipo discord

    creator = models.ForeignKey(AUTH_USER_MODEL, editable=False, related_name='squad_creator', on_delete=models.CASCADE)
    host = models.ForeignKey(AUTH_USER_MODEL, related_name='squad_host', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='squad_schedule', on_delete=models.CASCADE)
    
    members = models.ManyToManyField(AUTH_USER_MODEL, through='SquadMember', related_name='squad_members')
    banned_users = models.ManyToManyField(AUTH_USER_MODEL, through='SquadBan', related_name='squad_banned_users')

    @classmethod
    def create(cls, **kwargs):
        cls._validate(**kwargs)

        schedule = Schedule.create()
        squad = Squad.objects.create(tag=AbstractGroup.tag_creator(), schedule=schedule, **kwargs)
        squad.add(squad.host)

        return squad
    
    def create_event(self, **kwargs):
        Event.create(group=self, **kwargs)

    def get_events(self):
        return self.event_set.all()


class Event(AbstractGroup):
    
    squad = models.ForeignKey(Squad, blank=True, null=True, on_delete=models.CASCADE)  # Para que um squad possa criar eventos de jogos
    
    creator = models.ForeignKey(AUTH_USER_MODEL, editable=False, related_name='event_creator', on_delete=models.CASCADE)
    host = models.ForeignKey(AUTH_USER_MODEL, related_name='event_host', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='event_schedule', on_delete=models.CASCADE)

    members = models.ManyToManyField(AUTH_USER_MODEL, through='EventMember', related_name='event_members')
    banned_users = models.ManyToManyField(AUTH_USER_MODEL, through='EventBan', related_name='event_banned_users')

    @classmethod
    def create(cls, **kwargs):
        cls._validate(**kwargs)

        schedule = Schedule.create()
        event = Event.objects.create(tag=AbstractGroup.tag_creator(), schedule=schedule, **kwargs)
        event.add(event.host)

        return event
    
"""Relationship classes"""
class SquadMember(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='squad_member_user', on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, related_name='squad_member_squad', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in squad {self.squad.name}"


class EventMember(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='event_member_user', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='event_member_event', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in event {self.event.name}"


class SquadBan(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='squad_ban_user', on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, related_name='squad_ban_squad', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} banned in squad {self.squad.name}"


class EventBan(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, related_name='event_ban_user', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, related_name='event_ban_event', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} banned in event {self.event.name}"