from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as lazy

from django_countries.fields import CountryField

from games.models import Game
from core.models import DefaultFields, DefaultFieldsUserRelated
from schedule.models import ModelWithSchedule
from groups.models import Squad, Event


class User(DefaultFieldsUserRelated, AbstractUser, ModelWithSchedule): 

    class Plan(models.TextChoices):
        FREE = 'FREE', lazy('Free')
        PRO = 'PRO', lazy('Pro')

    class Status(models.TextChoices):
        ACTIVE = 'ACT', lazy('Active')
        SUSPENDED = 'SUS', lazy('Suspended')
        BANNED = 'BAN', lazy('Banned')

    email = models.EmailField(lazy("email address"), unique=True)
    
    country = CountryField(blank=False)
    dark_mode = models.BooleanField(default=True)       # Eventualmente dá para trocar ou adicionar algo como color: codigo_rgb
    profile_picture = models.ImageField(default='default_pfp.jpg', upload_to='profile_pics')

    """Campos que costumavam estar em player"""
    ban_request = models.BooleanField(default=False)
    discord = models.CharField(max_length=30)
    plan = models.CharField(max_length=4, choices=Plan, default=Plan.FREE)
    status = models.CharField(max_length=3, choices=Status, default=Status.ACTIVE)
    # notifications: https://github.com/django-notifications/django-notifications

    # game_preferences = models.ManyToManyField(Game)

    blocked_players = models.ManyToManyField('self', through='Block', symmetrical=False)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'country', 'first_name', 'last_name', ]  # O email não está sendo pedido por padrão.....

    # Lembrar de direcionar users recém registrados para uma tela de engajamento
    
    def __str__(self):
        return self.username or self.email

# Tabela intermediária de User em um relacionamento n pra n recursivo
class Friendship(DefaultFieldsUserRelated):
    '''
    Quais campos (metadados) podem ser úteis nessa tabela?
    Lembrar que os campos default já estão sendo herdados
    
    O campo active, nesse caso, considerando que o relacionamento é único entre instâncias,
    provavelmente vai ser usado para determinar se a amizade está ativa depois que foi criada.
    O mesmo é válido para as outras tabelas
    '''

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"], name="unique_constraint_friendship"
            )
        ]

    user_1 = models.ForeignKey(User, related_name='friendship_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='friendship_user_2', on_delete=models.CASCADE)

# Seguindo a ideia que eu pesquisei para a tabela de amizades, parece justo também fazer outras tabelas para os outros campos
class Block(DefaultFieldsUserRelated):
    blocking = models.ForeignKey(User, related_name='block_blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='block_blocked', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["blocking", "blocked"], name="unique_constraint_block"
            )
        ]

# A lógica parece certa...
# Talvez seja mais correto mudar essa tabela para outro campo, pelas boas práticas
class Silenced(DefaultFieldsUserRelated):
    # Talvez mudar esse nome...
    agent = models.ForeignKey(User, related_name='silenced_agent', on_delete=models.CASCADE)

    player = models.ForeignKey(User, related_name='silenced_player', null=True, blank=True, on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, related_name='silenced_squad', null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='silenced_event', null=True, blank=True, on_delete=models.CASCADE)

    @property
    def holder(self):
        return self.player or self.squad or self.event
    
    @holder.setter
    def holder(self, obj):
        if type(obj) == User:
            self.player = obj
            self.squad, self.event = None, None
        elif type(obj) == Event:
            self.event = obj
            self.squad, self.player = None, None
        elif type(obj) == Squad:
            self.squad = obj
            self.player, self.event = None, None
        else:
            raise ValueError("obj parameter must be an object of User, Squad or Event class")