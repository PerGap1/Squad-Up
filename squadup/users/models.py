from django.db import models
from django.contrib.auth.models import AbstractUser
from games.models import Game
from core.models import DefaultFieldsUserRelated, DefaultFields

from django.utils.translation import gettext_lazy as lazy
from django_countries.fields import CountryField

class User(DefaultFieldsUserRelated, AbstractUser): 

    class Plan(models.TextChoices):
        FREE = 'FR', lazy('Free')
        PRO = 'PR', lazy('Pro')

    class Status(models.TextChoices):
        ACTIVE = 'AT', lazy('Active')
        SUSPENDED = 'SP', lazy('Suspended')
        BANNED = 'BN', lazy('Banned')

    email = models.EmailField(lazy("email address"), unique=True)
    
    country = CountryField()
    dark_mode = models.BooleanField(default=True)
    profile_picture = models.ImageField()

    # Campos que costumavam estar em player
    ban_request = models.BooleanField(default=False)
    discord = models.CharField(max_length=30)
    plan = models.CharField(max_length=2, choices=Plan, default=Plan.FREE)
    status = models.CharField(max_length=2, choices=Status, default=Status.ACTIVE)
    # notifications: https://github.com/django-notifications/django-notifications
    # schedule = ?

    game_preferences = models.ManyToManyField(Game)

    # Atributos em relacionamento n pra n recursivo
    blocked_players = models.ManyToManyField('self', through='Block', symmetrical=False)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=True)
    # silenced = ?      # players, groups e events
    
    USERNAME_FIELD = 'email'        # Não gostei da forma que o usuário aparece...
    REQUIRED_FIELDS = ['username', 'country']

    # Lembrar de direcionar users recém registrados para uma tela de engajamento

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

# Falta Silenced, porém provavelmente haverá três classes silenced, uma pra cada tipo de objeto.
# Ou duas, considerando que Events e Squads herdam de uma classe abstrata