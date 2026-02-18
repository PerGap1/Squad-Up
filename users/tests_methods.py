from django.test import TestCase
from .models import User
from .tests import UserModelTests

class UserModelMethodsTests(TestCase):
        
    def setUp(self):
        UserModelTests.setUp()

    def test_user_invert_color(self):
        user = User.objects.first()
        dark_mode = user.dark_mode

        user.invert_color()
        self.assertNotEqual(dark_mode, user.dark_mode)

    def test_user_make_pro(self):
        user = User.objects.first()

        user.make_pro()
        self.assertEqual(user.plan.__str__(), 'PRO')

    def test_user_make_free(self):
        user = User.objects.first()

        user.make_pro()
        user.make_free()
        self.assertEqual(user.plan.__str__(), 'FREE')

    def test_user_ask_to_ban(self):
        user = User.objects.first()

        user.ask_to_ban()
        self.assertTrue(user.ban_request)

    def test_user_suspend(self):
        user = User.objects.first()

        user.suspend()
        self.assertEqual(user.status.__str__(), 'SUS')

    def test_user_ban(self):
        user = User.objects.first()

        user.ban()
        self.assertEqual(user.status.__str__(), 'BAN')

    def test_user_active(self):
        user = User.objects.first()

        user.ban()
        user.restore()
        self.assertEqual(user.status.__str__(), 'ACT')