from django.db import models
from core.models import DefaultFields
from django.utils.translation import gettext_lazy as lazy


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
    
    def new_availability(self, **kwargs): 
        return Availability.objects.create(schedule=self, **kwargs)
    
    def get_avails(self):
        return self.availability_schedule.all()
        
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

    REQUIRED_FIELDS = ['schedule', 'day_of_week', 'start_time', 'end_time']

    def save(self, **kwargs):
        not_given = []
        for field in self.REQUIRED_FIELDS:
            if not hasattr(self, field) or not getattr(self, field):
                not_given.append(field)

        if not_given:
            raise ValueError(f"Some required field(s) were not passed: {', '.join(not_given)}")
        
        return super().save(**kwargs)
    
    def delete(self):           # Talvez deprecate
        if not self.active:
            raise ValueError("Coudn't delete an availability: already deleted")
        self.active = False

    def is_compatible(self, other):
        return self.are_compatible(first=self, second=other)

    @classmethod
    def are_compatible(cls, first:Availability, second:Availability):
        first = first.start_time.minute + 10
        second = second.start_time.minute + 10
        return cls._verify_condition(first, second) or cls._verify_condition(second, first)

    @staticmethod
    def _verify_condition(first, second):
        condition_1 = first.start_time < second.end_time
        condition_2 = first.end_time > second.start_time

        return condition_1 and condition_2 and first.day_of_week == second.day_of_week

    def __str__(self):
        return f'{self.day_of_week}, {self.start_time} to {self.end_time}'