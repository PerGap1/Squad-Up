from core.models import DefaultFields
from django.db import models
from .models import User


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