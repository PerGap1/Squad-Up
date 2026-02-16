'''from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from groups.models import Squad, Event
from .models import Schedule


@receiver(post_save, sender=Squad)
@receiver(post_save, sender=Event)
@receiver(post_save, sender=get_user_model())
def update_schedule(sender, instance, created, **kwargs): 
    if created or not hasattr(instance, 'schedule'):
        print(instance)
        Schedule.objects.create(holder=instance)
    else:
        instance.schedule.save()'''