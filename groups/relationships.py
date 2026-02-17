from core.models import DefaultFields
from django.db import models
from squadup.settings import AUTH_USER_MODEL
from .models import Squad, Event


class SquadMember(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='squad_member_user', on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, related_name='squad_member_squad', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in squad {self.squad.name}"


class EventMember(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='event_member_user', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='event_member_event', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in event {self.event.name}"


class SquadBan(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='squad_ban_user', on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, related_name='squad_ban_squad', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} banned in squad {self.squad.name}"


class EventBan(DefaultFields):

    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, related_name='event_ban_user', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, related_name='event_ban_event', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} banned in event {self.event.name}"