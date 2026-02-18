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

    def __str__(self):
        return f'{self.day_of_week}, {self.start_time} to {self.end_time}'