from django.apps import AppConfig
from django.core.signals import request_finished


class ScheduleConfig(AppConfig):
    name = 'schedule'