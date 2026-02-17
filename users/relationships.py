from core.models import DefaultFields
from django.db import models
from .models import User


class Friendship(DefaultFields):
    user_1 = models.ForeignKey(User, related_name='friendship_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='friendship_user_2', on_delete=models.CASCADE)


class Block(DefaultFields):
    blocking = models.ForeignKey(User, related_name='block_blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='block_blocked', on_delete=models.CASCADE)
    

class MutedUser(DefaultFields):
    agent = models.ForeignKey(User, related_name='muted_user_agent', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='muted_user', on_delete=models.CASCADE)
    

class MutedSquad(DefaultFields):
    agent = models.ForeignKey(User, related_name='muted_squad_agent', on_delete=models.CASCADE)
    squad = models.ForeignKey('groups.Squad', related_name='muted_squad', on_delete=models.CASCADE)
    

class MutedEvent(DefaultFields):
    agent = models.ForeignKey(User, related_name='muted_event_agent', on_delete=models.CASCADE)
    event = models.ForeignKey('groups.Event', related_name='muted_event', on_delete=models.CASCADE)