from django.db import models
from core.models import DefaultFieldsUserRelated
from django.utils.translation import gettext_lazy as lazy


class Availability(DefaultFieldsUserRelated):

    class DayOfWeek(models.TextChoices):
        SUNDAY = 'SU', lazy('Sunday')
        MONDAY = 'MO', lazy('Monday')
        TUESDAY = 'TU', lazy('Tuesday')
        WEDNESDAY = 'WE', lazy('Wednesday')
        THURSDAY = 'TH', lazy('Thursday')
        FRIDAY = 'FR', lazy('Friday')
        SATURDAY = 'SA', lazy('Saturday')

    # day_of_week = models.DateField(), ou
    day_of_week = models.TextField(max_length=2, choices=DayOfWeek, blank=False)
    start_time = models.TimeField()
    end_time = models.TimeField()