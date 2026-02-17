from django.db import models
from core.models import DefaultFields
from django.utils.translation import gettext_lazy as lazy

from squadup.settings import AUTH_USER_MODEL


class ScheduleManager(models.Manager):

    def create(self, *args, **kwargs):
        if not kwargs.get('holder'):
            raise ValueError("Schedule's manager expects a holder to own the schedule")
        
        return super().create(*args, **kwargs)


class Schedule(DefaultFields):

    objects = ScheduleManager()
        
    def __str__(self): pass
        # return f"{self.holder}'s schedule"


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