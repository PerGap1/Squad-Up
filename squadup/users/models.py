from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 
    """
    Contry, dark mode...

    Como player, preciso ver se irei fazer OneToOneField, ou se vou colocar as informações aqui mesmo

    Player: ban request, blocked players, discord, friends, game preferences, notifications, plan, schedule,
    silenced events/groups/players, status (ban/suspended/active), first time(?)

    Colocar email como autenticador
    """
    profile_picture = models.ImageField()