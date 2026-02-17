from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as OriginalUserManager
from django.utils.translation import gettext_lazy as lazy

from django_countries.fields import CountryField
from abc import abstractmethod

from games.models import Game
from core.models import DefaultFields
from schedule.models import Schedule

# Sendo bem sincero, acho que extender UserManager pode ser uma má ideia, mas parece estar funcionando normalmente
class UserManager(OriginalUserManager):
    # Existem outras ideias interessantes para um object manager, para auxiliar em alguma coisa

    def create_schedule(user):
        if not user.schedule:
            user.schedule = Schedule.objects.create(holder=user)

    # Está ficando um pouquinho ridículo...
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        UserManager.create_schedule(user)
        return user
    
    def acreate(self, *args, **kwargs):
        user = super().acreate(*args, **kwargs)
        UserManager.create_schedule(user)
        return user
    
    def create_user(self, username, email = ..., password = ..., **extra_fields):
        user = super().create_user(username, email, password, **extra_fields)
        UserManager.create_schedule(user)
        return user
    
    def acreate_user(self, username, email = ..., password = ..., **extra_fields):
        user = super().acreate_user(username, email, password, **extra_fields)
        UserManager.create_schedule(user)
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        user = super().create_superuser(username, email, password, **extra_fields)
        UserManager.create_schedule(user)
        return user

    def acreate_superuser(self, username, email, password, **extra_fields):
        user = super().acreate_superuser(username, email, password, **extra_fields)
        UserManager.create_schedule(user)
        return user
    # Quando um superuser é criado a partir da linha de comando, ele vem sem schedule
    

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

    game_preferences = models.ManyToManyField(Game)

    blocked_players = models.ManyToManyField('self', through='Block', symmetrical=False)    # Nome longo...
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=True)

    schedule = models.OneToOneField('schedule.Schedule', null=True, related_name='user_schedule', on_delete=models.CASCADE)

    # Não gostei desse modelo, talvez tenha outro jeito
    silenced_players = models.ManyToManyField('self', through='SilencedPlayer', related_name='user_silenced_players', symmetrical=False)
    silenced_squads = models.ManyToManyField('groups.Squad', through='SilencedSquad', related_name='user_silenced_squads', symmetrical=False)
    silenced_events = models.ManyToManyField('groups.Event', through='SilencedEvent', related_name='user_silenced_events', symmetrical=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'country', 'first_name', 'last_name', ]

    # Lembrar de direcionar users recém registrados para uma tela de engajamento
    
    def __str__(self):
        return self.username or self.email


# Tabela intermediária de User em um relacionamento n pra n recursivo
class Friendship(DefaultFields):
    '''
    Quais campos (metadados) podem ser úteis nessa tabela?
    Lembrar que os campos default já estão sendo herdados
    
    O campo active, nesse caso, considerando que o relacionamento é único entre instâncias,
    provavelmente vai ser usado para determinar se a amizade está ativa depois que foi criada.
    O mesmo é válido para as outras tabelas
    '''

    '''class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"], name="unique_constraint_friendship"
            )
        ]'''

    user_1 = models.ForeignKey(User, related_name='friendship_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='friendship_user_2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Friendship between {self.user_1} and {self.user_2}'

# Seguindo a ideia que eu pesquisei para a tabela de amizades, parece justo também fazer outras tabelas para os outros campos
class Block(DefaultFields):

    '''class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["blocking", "blocked"], name="unique_constraint_block"
            )
        ]'''
    
    blocking = models.ForeignKey(User, related_name='block_blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='block_blocked', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_1} blocked {self.user_2}'
    

class SilencedPlayer(DefaultFields):

    agent = models.ForeignKey(User, related_name='silenced_player_agent', on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name='silenced_player', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.agent} silenced Player {self.player}'
    
class SilencedSquad(DefaultFields):

    agent = models.ForeignKey(User, related_name='silenced_squad_agent', on_delete=models.CASCADE)
    squad = models.ForeignKey('groups.Squad', related_name='silenced_squad', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.agent} silenced Event {self.squad}'
    
class SilencedEvent(DefaultFields):
    
    agent = models.ForeignKey(User, related_name='silenced_event_agent', on_delete=models.CASCADE)
    event = models.ForeignKey('groups.Event', related_name='silenced_event', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.agent} silenced Player {self.event}'