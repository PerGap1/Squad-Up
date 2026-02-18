from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as OriginalUserManager
from django.utils.translation import gettext_lazy as lazy

from django_countries.fields import CountryField

from games.models import Game
from groups.models import Squad, Event
from core.models import DefaultFields
from schedule.models import Schedule
    

class User(DefaultFields, AbstractUser): 

    class Plan(models.TextChoices):
        FREE = 'FREE', lazy('Free')
        PRO = 'PRO', lazy('Pro')

    class Status(models.TextChoices):
        ACTIVE = 'ACT', lazy('Active')
        SUSPENDED = 'SUS', lazy('Suspended')
        BANNED = 'BAN', lazy('Banned')

    email = models.EmailField(lazy("email address"), unique=True)
    
    country = CountryField()
    dark_mode = models.BooleanField(default=True)       # Eventualmente dá para trocar ou adicionar algo como color: codigo_rgb
    profile_picture = models.ImageField(default='default_pfp.jpg', upload_to='profile_pics')

    """Campos que costumavam estar em player"""
    ban_request = models.BooleanField(default=False)
    discord = models.CharField(max_length=30)
    plan = models.CharField(max_length=4, choices=Plan, default=Plan.FREE)
    status = models.CharField(max_length=3, choices=Status, default=Status.ACTIVE)
    # notifications: https://github.com/django-notifications/django-notifications

    games = models.ManyToManyField(Game)

    blocked_users = models.ManyToManyField('self', through='Block', symmetrical=False)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=True)

    schedule = models.OneToOneField('schedule.Schedule', related_name='user_schedule', on_delete=models.CASCADE)

    muted_users = models.ManyToManyField('self', through='MutedUser', related_name='user_muted_users', symmetrical=False)
    muted_squads = models.ManyToManyField('groups.Squad', through='MutedSquad', related_name='user_muted_squads', symmetrical=False)
    muted_events = models.ManyToManyField('groups.Event', through='MutedEvent', related_name='user_muted_events', symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'country', 'first_name', 'last_name']

    # Lembrar de direcionar users recém registrados para uma tela de engajamento

    @classmethod
    def create(cls, **kwargs):
        not_given = []
        for field in cls.REQUIRED_FIELDS + ['email']:
            if not kwargs.get(field):
                not_given.append(field)

        if not_given:
            raise ValueError(f"Some required field(s) were not passed: {', '.join(not_given)}")
        
        return User.objects.create(schedule=Schedule.create(), **kwargs)
    
    """Methods that don't operate with relational attributes"""
    def invert_color(self):
        if self.dark_mode: self.dark_mode = False
        else: self.dark_mode = True
    
    def delete(self):
        if not self.active:
            raise ValueError(f"Coudn't delete user {self}: already deleted")
        self.active = False

    def change_plan(self, plan):
        plan = plan.upper()

        if self.plan == plan:
            raise ValueError(f"User {self} is already on {plan.capitalize()} plan")
        if plan == 'PRO':
            self.plan = User.Plan.PRO
        elif plan == 'FREE':
            self.plan = User.Plan.FREE
        else:
            raise TypeError(f"Wrong type of plan passed to function 'change_plan'")

    def ask_to_ban(self): self.ban_request = True

    def restore(self): self.status = User.Status.ACTIVE

    def suspend(self):
        if self.status == User.Status.SUSPENDED or self.status == User.Status.SUSPENDED:
            raise ValueError(f"User is already {self.status}")
        self.status = User.Status.SUSPENDED

    def ban(self):
        if self.status == User.Status.BANNED:
            raise ValueError(f"User is already {self.status}")
        self.status = User.Status.BANNED

    """Methods to add and remove games and friends"""
    def add(self, object): 
        obj_type = type(object)
        if obj_type == User: User._add_friend(object)
        elif obj_type == Game: User._add_game(object)
        else:
            raise TypeError(f"Object of User or Game class expected, got {obj_type} instead")
    
    def add_many(self, objects): 
        for object in objects:
            User.add(object)

    def remove(self, object): 
        obj_type = type(object)
        if obj_type is User: User._remove_friend(object)
        elif obj_type is Game: User._remove_game(object)
        else:
            raise TypeError(f"Object of User or Game type expected, got {obj_type} instead")
    
    def remove_many(self, objects): 
        for object in objects:
            User.remove(object)

    """Methods to block users"""
    def block(self, user): 
        if user in self.blocked_users.all():
            raise ValueError(f"Coudn't block user {user}: already blocked")
        if not type(user) is User:
            raise TypeError(f"Object of User type expected, got {type(user)} instead")
        
        if user in self.friends.all():
            User._remove_friend(user)
        self.blocked_users.add(user)

    def block_many(self, users):
        for user in users: 
            User.block(user)

    def unblock(self, user): 
        if user not in self.blocked_users.all():
            raise ValueError(f"Coudn't unblock user {user}: not blocked")
        if not type(user) is User:
            raise TypeError(f"Object of User type expected, got {type(user)} instead")
        
        self.blocked_users.remove(user)

    def unblock_many(self, users):
        for user in users: 
            User.unblock(user)

    """Muting methods"""
    def mute(self, object): 
        obj_type = type(object)

        if obj_type is User:
            self.muted_users.add(object)
        elif obj_type is Squad:
            self.muted_squads.add(object)
        elif obj_type is Event:
            self.muted_squads.add(object)
        else:
            raise TypeError(f"Object of User, Squad or Event type expected, got {obj_type} instead")
        
    def mute_many(self, objects):
        for object in objects:
            User.mute(object)
    
    def unmute(self, object):
        obj_type = type(object)

        if obj_type is User:
            self.muted_users.remove(object)
        elif obj_type is Squad:
            self.muted_squads.remove(object)
        elif obj_type is Event:
            self.muted_squads.remove(object)
        else:
            raise TypeError(f"Object of User, Squad or Event type expected, got {obj_type} instead")

    def unmute_many(self, objects):
        for object in objects:
            User.unmute(object)

    """Private methods"""
    def _add_game(self, game): 
        if game in self.games.all():
            raise ValueError(f"Coudn't add {game.name} to user {self}' games: already in there")
        self.games.add(game)

    def _remove_game(self, game):
        if not game in self.games.all():
            raise ValueError(f"Coudn't remove {game.name} from user {self}' games: not in there")
        self.games.remove(game)

    def _add_friend(self, user):
        if user in self.friends.all():
            raise ValueError(f"Coudn't add user {user}: already friends")
        self.friends.add(user)

    def _remove_friend(self, user):
        if not user in self.friends.all():
            raise ValueError(f"Coudn't remove user {user}: not friends")
        self.friends.remove(user)
    
    def __str__(self):
        return self.username or self.email
    
"""Relationship classes"""
class Friendship(DefaultFields):
    user_1 = models.ForeignKey(User, related_name='friendship_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='friendship_user_2', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_2} is a friend of {self.user_2}"


class Block(DefaultFields):
    blocking = models.ForeignKey(User, related_name='block_blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='block_blocked', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blocking} blocked {self.blocked}"
    

class MutedUser(DefaultFields):
    muting = models.ForeignKey(User, related_name='muted_user_muting', on_delete=models.CASCADE)
    muted = models.ForeignKey(User, related_name='muted_user_muted', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.muting} muted user {self.user}"
    

class MutedSquad(DefaultFields):
    muting = models.ForeignKey(User, related_name='muted_squad_muting', on_delete=models.CASCADE)
    muted = models.ForeignKey('groups.Squad', related_name='muted_squad_muted', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.muting} muted squad {self.squad}"
    

class MutedEvent(DefaultFields):
    muting = models.ForeignKey(User, related_name='muted_event_muting', on_delete=models.CASCADE)
    muted = models.ForeignKey('groups.Event', related_name='muted_event_muted', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.muting} muted event {self.event}"