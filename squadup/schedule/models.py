from django.db import models
from core.models import DefaultFieldsUserRelated
from django.utils.translation import gettext_lazy as lazy

from users.models import User
from groups.models import Squad, Event


class Schedule(DefaultFieldsUserRelated):
    # Lembrar de criar um signals.py, para garantir que exista um object.schedule mesmo logo após a sua criação

    player = models.ForeignKey(User, blank=True, null=True)
    squad = models.ForeignKey(Squad, blank=True, null=True)
    event = models.ForeignKey(Event, blank=True, null=True)

    @property
    def holder(self):           # Não gostei do nome
        return self.player or self.squad or self.event
    
    @holder.setter
    def holder(self, obj):
        if type(obj) == User:
            self.player = obj
            self.squad, self.event = None, None
        elif type(obj) == Squad:
            self.squad = obj
            self.player, self.event = None, None
        elif type(obj) == Event:
            self.event = obj
            self.squad, self.player = None, None
        else:
            raise ValueError("obj parameter must be an object of User, Squad or Event class")


class Availability(DefaultFieldsUserRelated):

    class DayOfWeek(models.IntegerChoices):
        SUNDAY = 0, lazy('Sunday')
        MONDAY = 1, lazy('Monday')
        TUESDAY = 2, lazy('Tuesday')
        WEDNESDAY = 3, lazy('Wednesday')
        THURSDAY = 4, lazy('Thursday')
        FRIDAY = 5, lazy('Friday')
        SATURDAY = 6, lazy('Saturday')

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    day_of_week = models.IntegerField(choices=DayOfWeek)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.day_of_week}, {self.start_time} to {self.end_time}'