from django.test import TestCase

from .models import User


class UserModelTests(TestCase):

    @staticmethod
    def setUp():
        User.objects.create(
            username='squadup', 
            email='squadup@gmail.com',
            password='squadup255',
            country='BR',
            first_name='Squad',
            last_name='Up',
            )

    '''Jogar todos esses para seus próprios suítes'''
    '''def test_squad_not_created(self):
        squad = None
        try:
            squad = Squad.objects.create()
        except ValueError as e: 
            self.assertIsNone(squad)
        else:
            raise

    def test_event_not_created(self):
        event = None
        try:
            event = Event.objects.create()
        except ValueError as e: 
            self.assertIsNone(event)
        else:
            raise

    def test_game_not_created(self):
        game = None
        try:
            game = Game.objects.create()
        except ValueError: 
            self.assertIsNone(game)
        else:
            raise
'''