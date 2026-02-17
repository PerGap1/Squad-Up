from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as OriginalUserManager
from django.utils.translation import gettext_lazy as lazy

from django_countries.fields import CountryField

from games.models import Game
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

    blocked_users = models.ManyToManyField('self', through='Block', symmetrical=False)      # Aqui agora
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=True)

    schedule = models.OneToOneField('schedule.Schedule', null=False, related_name='user_schedule', on_delete=models.CASCADE)

    silenced_users = models.ManyToManyField('self', through='SilencedUser', related_name='user_silenced_users', symmetrical=False)
    silenced_squads = models.ManyToManyField('groups.Squad', through='SilencedSquad', related_name='user_silenced_squads', symmetrical=False)
    silenced_events = models.ManyToManyField('groups.Event', through='SilencedEvent', related_name='user_silenced_events', symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'country', 'first_name', 'last_name', ]

    # Lembrar de direcionar users recém registrados para uma tela de engajamento

    @staticmethod
    def create(**kwargs):
        return User.objects.create(schedule=Schedule.create(), **kwargs)
    
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

    def add_game(self, game): 
        User._add_game(game)

    def add_many_games(self, games):
        for game in games:
            User._add_game(game)

    def remove_game(self, game): 
        User._remove_game(game)

    def remove_many_games(self, games):
        for game in games:
            User._remove_game(game)

    def ask_to_ban(self):
        self.ban_request = True

    def restore(self):
        self.status = User.Status.ACTIVE

    def suspend(self):
        if self.status == User.Status.SUSPENDED or self.status == User.Status.SUSPENDED:
            raise ValueError(f"User is already {self.status}")
        self.status = User.Status.SUSPENDED

    def ban(self):
        if self.status == User.Status.BANNED:
            raise ValueError(f"User is already {self.status}")
        self.status = User.Status.BANNED

    """Private methods"""
    def _add_game(self, game): 
        if game in self.games.all():
            raise ValueError(f"Coudn't add {game.name} to user {self}' games: already in there")
        self.games.add(game)

    def _remove_game(self, game):
        if not game in self.games.all():
            raise ValueError(f"Coudn't remove {game.name} from user {self}' games: not in there")
        self.games.remove(game)
    
    def __str__(self):
        return self.username or self.email