from django.db import models
from core.models import DefaultFields
from django.utils.translation import gettext_lazy as lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from squadup.settings import AUTH_USER_MODEL


class ScheduleManager(models.Manager):

    def create(self, *args, **kwargs):
        if not kwargs.get('holder'):
            raise ValueError("Schedule's manager expects a holder to own the schedule")
        
        return super().create(*args, **kwargs)


class Schedule(DefaultFields):

    player = models.OneToOneField(AUTH_USER_MODEL, blank=True, null=True, related_name='schedule_player', on_delete=models.CASCADE)
    squad = models.OneToOneField('groups.Squad', blank=True, null=True, related_name='schedule_squad', on_delete=models.CASCADE)
    event = models.OneToOneField('groups.Event', blank=True, null=True, related_name='schedule_event', on_delete=models.CASCADE)

    objects = ScheduleManager()

    # Estou com a impressão de que User ter schedule e schedule ter holder não é uma boa ideia
    @property
    def holder(self):           # Não gostei do nome
        result = self.player or self.squad or self.event
        if not result:
            raise ValueError("Schedule's holder has not been set")
        return 
    
    @holder.setter
    def holder(self, obj):
        error_msg = f"obj parameter must be an object of User, Squad or Event class, {type(obj)} was passed"

        if not hasattr(obj, 'get_class'):
            raise ValueError(error_msg)
        
        if obj.get_class() == 'User':
            self.player = obj
            self.squad, self.event = None, None
        elif obj.get_class() == 'Squad':
            self.squad = obj
            self.event, self.player = None, None
        elif obj.get_class() == 'Event':
            self.event = obj
            self.player, self.squad = None, None
        else:
            raise ValueError(error_msg)
        
    def __str__(self):
        return f"{self.holder}'s schedule"


class Availability(DefaultFields):

    class DayOfWeek(models.IntegerChoices):
        SUNDAY = 0, lazy('Sunday')
        MONDAY = 1, lazy('Monday')
        TUESDAY = 2, lazy('Tuesday')
        WEDNESDAY = 3, lazy('Wednesday')
        THURSDAY = 4, lazy('Thursday')
        FRIDAY = 5, lazy('Friday')
        SATURDAY = 6, lazy('Saturday')

    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name='availability_schedule')

    day_of_week = models.IntegerField(choices=DayOfWeek)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.day_of_week}, {self.start_time} to {self.end_time}'