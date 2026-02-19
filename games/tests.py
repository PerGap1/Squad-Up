from django.test import TestCase
import datetime
from users.models import User
from .models import Game


class GameModelTest(TestCase):

    def setUp(self):
        User.objects.create(
            username='squadup', 
            email='squadup@gmail.com',
            password='squadup255',
            country='BR',
            first_name='Squad',
            last_name='Up',
        )
        Game.objects.create(
            name='Game',
            released=datetime.datetime.now(),
            creator=User.objects.first(),
        )

    def test_game_not_created(self):
        game = None
        try:
            game = Game.objects.create()
        except ValueError: 
            self.assertIsNone(game)
        else:
            raise

    def test_game_required_attrs(self):
        game = Game.objects.first()

        self.assertHasAttr(game, 'name')
        self.assertHasAttr(game, 'released')
        self.assertHasAttr(game, 'creator')

    def test_game_holder_set(self):
        game = Game.objects.first()

        self.assertHasAttr(game, 'user_set')
        self.assertHasAttr(game, 'squad_set')
        self.assertHasAttr(game, 'event_set')