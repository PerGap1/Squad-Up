from django.test import TestCase
from .models import Squad, Event


class SquadModelTest(TestCase):
    def test_squad_not_created(self):
        squad = None
        try:
            squad = Squad.objects.create()
        except ValueError as e: 
            self.assertIsNone(squad)
        else:
            raise