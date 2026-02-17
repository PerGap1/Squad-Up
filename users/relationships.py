from core.models import DefaultFields
from django.db import models
from .models import User


class Friendship(DefaultFields):
    user_1 = models.ForeignKey(User, related_name='friendship_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='friendship_user_2', on_delete=models.CASCADE)


class Block(DefaultFields):
    blocking = models.ForeignKey(User, related_name='block_blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='block_blocked', on_delete=models.CASCADE)
    

class SilencedUser(DefaultFields):
    agent = models.ForeignKey(User, related_name='silenced_user_agent', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='silenced_user', on_delete=models.CASCADE)
    
class SilencedSquad(DefaultFields):
    agent = models.ForeignKey(User, related_name='silenced_squad_agent', on_delete=models.CASCADE)
    squad = models.ForeignKey('groups.Squad', related_name='silenced_squad', on_delete=models.CASCADE)
    

class SilencedEvent(DefaultFields):
    agent = models.ForeignKey(User, related_name='silenced_event_agent', on_delete=models.CASCADE)
    event = models.ForeignKey('groups.Event', related_name='silenced_event', on_delete=models.CASCADE)