from django.db import models
from core.models import DefaultFields
from django.utils.translation import gettext_lazy as lazy

import datetime


class Schedule(DefaultFields):

    @property
    def holder(self):
        if hasattr(self, 'user_schedule'): return self.user_schedule
        elif hasattr(self, 'squad_schedule'): return self.squad_schedule
        elif hasattr(self, 'event_schedule'): return self.event_schedule
        else: raise RuntimeError("This Schedule object has no holder")
    
    def delete(self):       # Talvez funções delete serão abandonadas
        if not self.active:
            raise ValueError(f"Coudn't delete {self}: already deleted")
        self.active = False
    
    def new_availability(self, *args, **kwargs): 
        return Availability.objects.create(schedule=self, *args, **kwargs)
    
    def get_avails(self):
        return self.availability_schedule.all()
        
    def __str__(self):
        return f"{self.holder}'s schedule"


class AvailabilityManager(models.Manager):

    def create(self, *args, **kwargs):
        if args and len(args) == 3:
            kwargs['day_of_week'] = args[0]
            kwargs['start_time'] = args[1]
            kwargs['end_time'] = args[2]
        super().create(**kwargs)


class Availability(DefaultFields):

    class DayOfWeek(models.IntegerChoices):
        SUNDAY = 0, lazy('Sunday')
        MONDAY = 1, lazy('Monday')
        TUESDAY = 2, lazy('Tuesday')
        WEDNESDAY = 3, lazy('Wednesday')
        THURSDAY = 4, lazy('Thursday')
        FRIDAY = 5, lazy('Friday')
        SATURDAY = 6, lazy('Saturday')

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='availability_schedule')

    day_of_week = models.IntegerField(choices=DayOfWeek)
    start_time = models.TimeField()
    end_time = models.TimeField()

    objects = AvailabilityManager()

    REQUIRED_FIELDS = ['schedule', 'day_of_week', 'start_time', 'end_time']

    def save(self, *args, **kwargs):
        not_given = []
        for field in self.REQUIRED_FIELDS:
            if not hasattr(self, field) or getattr(self, field) is None:
                not_given.append(field)

        if not_given:
            raise ValueError(f"Some required field(s) were not passed: {', '.join(not_given)}")
        
        self._validate_times()
        if not 0 <= self.day_of_week <= 6:
            raise ValueError("Invalid value for day of week")
        
        return super().save(**kwargs)
    
    def delete(self):
        if not self.active:
            raise ValueError("Coudn't delete an availability: already deleted")
        self.active = False

    def is_compatible(self, other):
        return self.are_compatible(first=self, second=other)

    @classmethod
    def are_compatible(cls, first:Availability, second:Availability):
        return cls._verify_condition(first, second) or cls._verify_condition(second, first)

    @staticmethod
    def _verify_condition(first, second):
        first_start_time = datetime.timedelta(
            hours=first.start_time.hour, 
            minutes=first.start_time.minute, 
            seconds=first.start_time.second
        )
        first_end_time = datetime.timedelta(
            hours=first.end_time.hour, 
            minutes=first.end_time.minute, 
            seconds=first.end_time.second
        )

        second_start_time = datetime.timedelta(
            hours=second.start_time.hour, 
            minutes=second.start_time.minute, 
            seconds=second.start_time.second
        )
        second_end_time = datetime.timedelta(
            hours=second.end_time.hour, 
            minutes=second.end_time.minute, 
            seconds=second.end_time.second
        )

        five_mins = datetime.timedelta(minutes=5)

        condition_1 = first_start_time + five_mins <= second_end_time - five_mins
        condition_2 = first_end_time - five_mins >= second_start_time + five_mins

        return condition_1 and condition_2 and first.day_of_week == second.day_of_week
    
    def _validate_times(self):
        start_time = datetime.timedelta(
            hours=self.start_time.hour, 
            minutes=self.start_time.minute, 
            seconds=self.start_time.second
        )
        end_time = datetime.timedelta(
            hours=self.end_time.hour, 
            minutes=self.end_time.minute, 
            seconds=self.end_time.second
        )

        if end_time < start_time:
            raise ValueError("Value for end time is lower than for start time")
        if end_time < start_time + datetime.timedelta(minutes=10):
            raise ValueError("Time between start time and end time is too low")

    def __str__(self):
        return f'{self.day_of_week}, {self.start_time} to {self.end_time}'