from django.db import models
from django.utils.translation import gettext_lazy as lazy

from abc import abstractmethod
from random import randint

from games.models import Game
from core.models import DefaultFields
from squadup.settings import AUTH_USER_MODEL
from schedule.models import Schedule


class AbstractGroup(DefaultFields):
    class Meta:
        abstract = True
    
    class Privacy(models.TextChoices):
        PUBLIC = 'PB', lazy('Public')
        LINKED = 'LK', lazy('Linked')
        PRIVATE = 'PR', lazy('Private')

    class ErrorMessages:
        ERROR_ADDING = "Coudn't add %s to group %s: already in there"
        ERROR_REMOVING = "Coudn't remove %s from group's %s: not in there"
        ERROR_PROMOTING = "Coudn't promote %s to host: already the host"
        ERROR_BANNING = "Cannot ban user %s: already banned"
        ERROR_DELETING = "Coudn't delete group %s: already deleted"

    name = models.CharField(max_length=50, null=False, blank=False)
    privacy = models.CharField(max_length=2, choices=Privacy, default=Privacy.PUBLIC, blank=False)
    tag = models.CharField(max_length=7, unique=True, editable=False, null=False, blank=False)
    image = models.ImageField(default='default_pfp.jpg', upload_to='profile_pics')

    games = models.ManyToManyField(Game)

    creator = ...
    host = ...
    members = ...
    banned_users = ...
    schedule = ...
    
    # chat...? Talvez importar um app chat, talvez criar nós mesmos e fazer um relacionamento 1 pra 1
    
    @staticmethod
    def tag_creator():      # É possível cair com uma tag obscena ou algo do tipo
        # Talvez dê para pensar em uma forma melhor, sem recursão
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
    
    """Related to members"""
    def add_user(self, user):
        AbstractGroup._add_user(user)

    def add_many_users(self, users):
        for user in users:
            AbstractGroup._add_user(user)

    def remove_user(self, user): 
        AbstractGroup._remove_user(user)

    def remove_many_users(self, users):
        for user in users:
            AbstractGroup._remove_user(user)

    def ban_user(self, user): 
        AbstractGroup._ban_user(user)

    def ban_many_users(self, users):
        for user in users:
            AbstractGroup._ban_user(user)   

    """Related to games"""
    def add_game(self, game): 
        AbstractGroup._add_game(game)

    def add_many_games(self, games):
        for game in games:
            AbstractGroup._add_game(game)

    def remove_game(self, game): 
        AbstractGroup._remove_game(game)

    def remove_many_games(self, games):
        for game in games:
            AbstractGroup._remove_game(game)
        
    """Private functions"""
    def _add_user(self, user):
        if user in self.members:
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_ADDING % (user.username, 'members'))
        self.members.add(user)

    def _remove_user(self, user):
        if not user in self.members.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_REMOVING % (user.username, 'members'))
        self.members.remove(user)

    def _ban_user(self, user):
        AbstractGroup._remove_user(user)

        if user in self.banned_users.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_BANNING % user.username)
        self.banned_users.add(user)

    def _add_game(self, game): 
        if game in self.games.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_ADDING % (game.name, 'games'))
        self.games.add(game)

    def _remove_game(self, game):
        if not game in self.games.all():
            raise ValueError(AbstractGroup.ErrorMessages.ERROR_REMOVING % (game.name, 'games'))
        self.games.remove(game)

    """Dunder methods"""
    def __str__(self):
        return self.name
    
    """Abstract methods"""
    @abstractmethod
    def create(self, *args, **kwargs): ...


class Squad(AbstractGroup): # Talvez permitir que um grupo tenha subgrupos, tipo discord

    creator = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, editable=False, related_name='squad_creator', on_delete=models.CASCADE)
    host = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, related_name='squad_host', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='squad_schedule', on_delete=models.CASCADE)
    
    members = models.ManyToManyField(AUTH_USER_MODEL, through='SquadMember', related_name='squad_members')
    banned_users = models.ManyToManyField(AUTH_USER_MODEL, through='SquadBan', related_name='squad_banned_users')

    @staticmethod
    def create(*args, **kwargs):
        schedule = Schedule.create()
        squad = Squad.objects.create(tag=AbstractGroup.tag_creator(), schedule=schedule, *args, **kwargs)
        return squad
    
    def create_event(self, *args, **kwargs):
        Event.create(group=self, *args, **kwargs)

    def get_events(self, *args, **kwargs):
        return self.event_set.all()


class Event(AbstractGroup):
    
    group = models.ForeignKey(Squad, blank=True, null=True, on_delete=models.CASCADE)  # Para que um grupo possa criar eventos de jogos
    
    creator = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, editable=False, related_name='event_creator', on_delete=models.CASCADE)
    host = models.ForeignKey(AUTH_USER_MODEL, null=False, blank=False, related_name='event_host', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedule.Schedule', null=True, blank=True, related_name='event_schedule', on_delete=models.CASCADE)

    members = models.ManyToManyField(AUTH_USER_MODEL, through='EventMember', related_name='event_members')
    banned_users = models.ManyToManyField(AUTH_USER_MODEL, through='EventBan', related_name='event_banned_users')

    @staticmethod
    def create(*args, **kwargs):
        schedule = Schedule.create()
        event = Event.objects.create(tag=AbstractGroup.tag_creator(), schedule=schedule, *args, **kwargs)
        return event