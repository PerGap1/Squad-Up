from django.db import models
from django.contrib.auth.models import AbstractUser
from games.models import Game

from django.utils.translation import gettext_lazy as lazy
from django_countries.fields import CountryField

class User(AbstractUser): 
    class Plan(models.TextChoices):
        FREE = 'FR', lazy('Free')
        PRO = 'PR', lazy('Pro')

    class Status(models.TextChoices):
        ACTIVE = 'AT', lazy('Active')
        SUSPENDED = 'SP', lazy('Suspended')
        BANNED = 'BN', lazy('Banned')

    # USERNAME_FIELD = email                            # Em teoria é assim que se coloca o email como o identificador...
                                                        # Porém não estou conseguindo acessar os atributos de dentro da classe
    
    country = CountryField()
    dark_mode = models.BooleanField(default=True)
    profile_picture = models.ImageField()

    # Campos que costumavam estar em player
    ban_request = models.BooleanField(default=False)    # Campos estão em ordem alfabética, talvez seja uma boa ideia mudar
    # blocked_players = models.ManyToManyField(User)      # <<<
    discord = models.CharField(max_length=30)
    # friends = models.ManyToManyField(User)              # <<<
    game_preferences = models.ManyToManyField(Game)     # Pesquisar diferença entre rel e field
    # notifications = ?
    plan = models.CharField(max_length=2, choices=Plan, default=Plan.FREE)
    # schedule = ?
    # silenced = ?                                      # players, groups e events
    status = models.CharField(max_length=2, choices=Status, default=Status.ACTIVE)
    first_time = models.BooleanField(default=True)      # AbstractUser já tem date joined, talvez dê pra dispensar esse campo


'''
class Staff(models.Model): 
    """
    Na verdade, tanto AbstractUser quanto as classes anteriores na cadeia de herança,
    possuem campos apenas para staff, tipo is_staff = False, is_superuser = False...
    O próprio Django oferece opções para nós, tanto em autenticação quanto em admin,
    então talvez essa classe seja desnecessária.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document = models.CharField(max_length=20)          # Não sei como fazer esse campo valer para todos os países
    # staff_type = models.TextField                     # Será necessário?
'''