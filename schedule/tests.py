from django.test import TestCase

import datetime

from users.models import User
from groups.models import Squad, Event
from .models import Schedule, Availability


class ScheduleModelTest(TestCase):

    def setUp(self):
        User.objects.create(
            username='squadup', 
            email='squadup@gmail.com',
            password='squadup255',
            country='BR',
            first_name='Squad',
            last_name='Up',
        )
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

    def test_schedule_holder(self):
        schedules = Schedule.objects.all()

        self.assertIsInstance(schedules[0].holder, User)
        self.assertIsInstance(schedules[1].holder, Squad)
        self.assertIsInstance(schedules[2].holder, Event)


class AvailabilityModelTest(TestCase):

    def setUp(self):
        user = User.objects.create(
            username='squadup', 
            email='squadup@gmail.com',
            password='squadup255',
            country='BR',
            first_name='Squad',
            last_name='Up',
        )
        user.schedule.new_availability(
            # Main availability
            day_of_week=0,
            start_time=datetime.time(12, 0, 0),
            start_time=datetime.time(16, 0, 0),
        )
        user.schedule.new_availability(
            # Starts when the first is ending
            day_of_week=0,
            start_time=datetime.time(15, 30, 0),
            start_time=datetime.time(19, 30, 0),
        )
        user.schedule.new_availability(
            # Ends when the first is starting
            day_of_week=0,
            start_time=datetime.time(8, 30, 0),
            start_time=datetime.time(12, 30, 0),
        )
        user.schedule.new_availability(
            # Starts and ends inside the first
            day_of_week=0,
            start_time=datetime.time(13, 30, 0),
            start_time=datetime.time(14, 30, 0),
        )
        user.schedule.new_availability(
            # Starts and ends outside the first
            day_of_week=0,
            start_time=datetime.time(11, 30, 0),
            start_time=datetime.time(16, 30, 0),
        )
        user.schedule.new_availability(
            # Starts and ends before the first
            day_of_week=0,
            start_time=datetime.time(6, 0, 0),
            start_time=datetime.time(8, 0, 0),
        )
        user.schedule.new_availability(
            # In a different day than the first
            day_of_week=2,
            start_time=datetime.time(12, 0, 0),
            start_time=datetime.time(16, 0, 0),
        )

    def test_availability_has_schedule(self):
        availability = Availability.objects.first()

        self.assertEqual(Schedule.objects.first(), availability.schedule)

    # Testar uma vez a are compatible

    def test_availability_start_compatible(self):
        schedule = User.objects.get(id=1).schedule
        first = schedule.get_avails()[0]
        second = schedule.get_avails()[1]

        self.assertTrue(first.is_compatible(second))

    def test_availability(): pass
    def test_availability(): pass
    def test_availability(): pass
    def test_availability(): pass