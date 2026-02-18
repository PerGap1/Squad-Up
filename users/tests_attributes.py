from django.test import TestCase
from .models import User
from .tests import UserModelTests

class UserModelAttributesTests(TestCase):
        
    def setUp(self):
        UserModelTests.setUp()
        
    def test_user_not_created(self):
        user = None
        try:
            user = User.objects.create()
        except ValueError as e: 
            self.assertIsNone(user)
        else:
            raise

    def test_user_required_attrs(self):
        user = User.objects.first()

        self.assertHasAttr(user, 'username')
        self.assertHasAttr(user, 'email')
        self.assertHasAttr(user, 'password')
        self.assertHasAttr(user, 'country')
        self.assertHasAttr(user, 'first_name')
        self.assertHasAttr(user, 'last_name')

    def test_user_has_schedule(self):
        user = User.objects.first()

        self.assertHasAttr(user, 'schedule')

    def test_user_dark_mode(self):
        user = User.objects.first()

        self.assertHasAttr(user, 'dark_mode')
        self.assertTrue(user.dark_mode)

    def test_user_ban_request(self):
        user = User.objects.first()

        self.assertHasAttr(user, 'ban_request')
        self.assertFalse(user.ban_request)

    def test_user_plan(self):
        user = User.objects.first()

        self.assertHasAttr(user, 'plan')
        self.assertEqual(user.plan.__str__(), 'FREE')

    def test_user_status(self):
        user = User.objects.first()

        self.assertHasAttr(user, 'status')
        self.assertEqual(user.status.__str__(), 'ACT')