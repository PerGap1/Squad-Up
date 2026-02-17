from django.db import models
from core.models import DefaultFields
from django.utils.translation import gettext_lazy as lazy


class Schedule(DefaultFields):

    def create(self, *args, **kwargs): 
        return self.objects.create(*args, **kwargs)
    
    def delete(self):
        if not self.active:
            raise ValueError(f"Coudn't delete {self}: already deleted")
        self.active = False

    def get_holder(self):
        return self.user_set.first() or self.squad_set.first() or self.event_set.first()
    
    def get_availabilities(self):
        return self.availability_set.all()
    
    def new_availability(self, **kwargs): 
        return Availability.create(schedule=self, **kwargs)
        
    def __str__(self):
        return f"{self.get_holder()}'s schedule"


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

    @classmethod
    def create(cls, **kwargs):
        return cls.objects.create(**kwargs)
    
    def delete(self):
        if not self.active:
            raise ValueError("Coudn't delete an availability: already deleted")
        self.active = False

    def __str__(self):
        return f'{self.day_of_week}, {self.start_time} to {self.end_time}'