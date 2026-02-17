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

    email = models.EmailField(lazy("email address"), unique=True, blank=False, null=False)
    
    country = CountryField(blank=False)
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

    schedule = models.OneToOneField('schedule.Schedule', null=False, related_name='user_schedule', on_delete=models.CASCADE)

    muted_users = models.ManyToManyField('self', through='MutedUser', related_name='user_muted_users', symmetrical=False)
    muted_squads = models.ManyToManyField('groups.Squad', through='MutedSquad', related_name='user_muted_squads', symmetrical=False)
    muted_events = models.ManyToManyField('groups.Event', through='MutedEvent', related_name='user_muted_events', symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'country', 'first_name', 'last_name', ]

    # Lembrar de direcionar users recém registrados para uma tela de engajamento

    @staticmethod
    def create(**kwargs):
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

    """Game methods"""
    def add_game(self, game): User._game_func(game=game, add=True)
    def add_many_games(self, games): [User._game_func(game=game, add=True) for game in games]

    def remove_game(self, game): User._game_func(game=game, add=False)
    def remove_many_games(self, games): [User._game_func(game=game, add=False) for game in games]

    """Friendship methods =P"""
    def add_friend(self, user): User._friend_func(user=user, add=True)
    def add_many_friends(self, users): [User._friend_func(user=user, add=True) for user in users]

    def remove_friend(self, user): User._friend_func(user=user, add=False)
    def remove_many_friends(self, users): [User._friend_func(user=user, add=False) for user in users]

    """Blocking methods"""
    def block_user(self, user): User._block_func(user=user, add=True)
    def block_many_users(self, users): [User._block_func(user=user, add=True) for user in users]

    def unblock_user(self, user): User._block_func(user=user, add=False)
    def unblock_many_users(self, users): [User._block_func(user=user, add=False) for user in users]

    """Muting methods"""
    def mute_user(self, user): User._mute_obj(object=user, add=True)
    def mute_many_users(self, users): [User._mute_obj(object=user, add=True) for user in users]

    def mute_squad(self, squad): User._mute_obj(object=squad, add=True)
    def mute_many_squads(self, squads): [User._mute_obj(object=squad, add=True) for squad in squads]

    def mute_event(self, event): User._mute_obj(object=event, add=True)
    def mute_many_events(self, events): [User._mute_obj(object=event, add=True) for event in events]

    def unmute_user(self, user): User._mute_obj(object=user, add=False)
    def unmute_many_users(self, users): [User._mute_obj(object=user, add=False) for user in users]

    def unmute_squad(self, squad): User._mute_obj(object=squad, add=False)
    def unmute_many_squads(self, squads): [User._mute_obj(object=squad, add=False) for squad in squads]

    def unmute_event(self, event): User._mute_obj(object=event, add=False)
    def unmute_many_events(self, events): [User._mute_obj(object=event, add=False) for event in events]

    """Private methods"""
    def _game_func(self, game, add): 
        if add:
            if game in self.games.all():
                raise ValueError(f"Coudn't add {game.name} to user {self}' games: already in there")
            self.games.add(game)
        else:
            if not game in self.games.all():
                raise ValueError(f"Coudn't remove {game.name} from user {self}' games: not in there")
            self.games.remove(game)

    def _block_func(self, user, add):
        if add:
            if user in self.blocked_users.all():
                raise ValueError(f"Coudn't block user {user}: already blocked")
            
            if user in self.friends.all():
                User._remove_friend(user)
            self.blocked_users.add(user)
        else:
            if user not in self.blocked_users.all():
                raise ValueError(f"Coudn't unblock user {user}: not blocked")
            self.blocked_users.remove(user)

    def _friend_func(self, user, add):
        if add:
            if user in self.friends.all():
                raise ValueError(f"Coudn't add user {user}: already friends")
            self.friends.add(user)
        else:
            if not user in self.friends.all():
                raise ValueError(f"Coudn't remove user {user}: not friends")
            self.friends.remove(user)

    def _mute_obj(self, object, add):
        if add:
            types = {User: self.muted_users, Squad: self.muted_squads, Event: self.muted_events}

            if object in types[type(object)].all():
                raise ValueError(f"Coudn't mute {type(object)} {object}: already muted")
            
            types[type(object)].add(object)
        else:
            types = {User: self.muted_users, Squad: self.muted_squads, Event: self.muted_events}

            if not object in types[type(object)].all():
                raise ValueError(f"Coudn't unmute {type(object)} {object}: already unmuted")
            
            types[type(object)].add(object)
    
    def __str__(self):
        return self.username or self.email