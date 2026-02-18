from django.test import TestCase

import datetime

from .models import User
from groups.models import Squad, Event
from games.models import Game
from .tests import UserModelTests

class UserModelRelationshipsTests(TestCase):
        
    def setUp(self):
        UserModelTests.setUp()

        Squad.objects.create(
            name='SquadUp',
            creator=User.objects.first(),
            host=User.objects.first(),
        )
        Event.objects.create(
            name='SquadUp',
            creator=User.objects.first(),
            host=User.objects.first(),
        )
        Game.objects.create(
            name='Game',
            released=datetime.datetime.now(),
            creator=User.objects.first(),
        )
        User.objects.create(
            username='squadup2', 
            email='squadup2@gmail.com',
            password='squadup255',
            country='BR',
            first_name='Squad',
            last_name='Up',
        )

    @staticmethod
    def _get_two_users():
        user_1 = User.objects.get(id=1)
        user_2 = User.objects.get(id=2)
        return user_1, user_2
    
    """User relationships"""
    def test_users_can_add_friend(self):
        user_1, user_2 = UserModelRelationshipsTests._get_two_users()
        user_1.add(user_2)

        self.assertEqual(user_1, user_2.friends.first())
        self.assertEqual(user_2, user_1.friends.first())

    def test_user_can_add_game(self):
        user_1 = User.objects.first()
        game = Game.objects.first()

        user_1.add(game)

        self.assertEqual(game, user_1.games.first())

    def test_user_can_block_user(self):
        user_1, user_2 = UserModelRelationshipsTests._get_two_users()
        user_1.block(user_2)

        self.assertEqual(user_2, user_1.blocked_users.first())
        self.assertFalse(user_2.blocked_users.all().exists())

    def test_user_can_mute_user(self):
        user_1, user_2 = UserModelRelationshipsTests._get_two_users()
        user_1.mute(user_2)

        self.assertEqual(user_2, user_1.muted_users.first())
        self.assertFalse(user_2.muted_users.all().exists())

    def test_user_can_mute_squad(self):
        user_1 = User.objects.first()
        squad = Squad.objects.first()

        user_1.mute(squad)

        self.assertEqual(squad, user_1.muted_squads.first())

    def test_user_can_mute_event(self):
        user_1 = User.objects.first()
        event = Event.objects.first()

        user_1.mute(event)

        self.assertEqual(event, user_1.muted_events.first())

    """User cancel relationships"""
    def test_users_can_remove_friend(self):
        user_1, user_2 = UserModelRelationshipsTests._get_two_users()
        user_1.add(user_2)
        user_1.remove(user_2)

        self.assertFalse(user_1.friends.all().exists())
        self.assertFalse(user_2.friends.all().exists())

    def test_user_can_remove_game(self):
        user_1 = User.objects.first()
        game = Game.objects.first()

        user_1.add(game)
        user_1.remove(game)

        self.assertFalse(user_1.games.all().exists())

    def test_user_can_unblock_user(self):
        user_1, user_2 = UserModelRelationshipsTests._get_two_users()
        user_1.block(user_2)
        user_1.unblock(user_2)

        self.assertFalse(user_1.blocked_users.all().exists())

    def test_user_can_unmute_user(self):
        user_1, user_2 = UserModelRelationshipsTests._get_two_users()
        user_1.mute(user_2)
        user_1.unmute(user_2)

        self.assertFalse(user_1.muted_users.all().exists())

    def test_user_can_unmute_squad(self):
        user_1 = User.objects.first()
        squad = Squad.objects.first()

        user_1.mute(squad)
        user_1.unmute(squad)

        self.assertFalse(user_1.muted_squads.all().exists())

    def test_user_can_unmute_event(self):
        user_1 = User.objects.first()
        event = Event.objects.first()

        user_1.mute(event)
        user_1.unmute(event)

        self.assertFalse(user_1.muted_events.all().exists())