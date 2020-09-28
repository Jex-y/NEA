import datetime

import django
from django.test import TestCase
from django.utils import timezone
from ..models import DailyMenu

class DailyMenuModelTests(TestCase):

    def setUp(self):
        start_time = datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        end_time = datetime.datetime.fromisoformat("2020-01-01T16:00:00")
        DailyMenu.objects.create(name="Test Menu", start_time=start_time, end_time=end_time)

    def test_menu_check_availability_correct_daily_time(self):
        """
        Menu.check_availability(time) should return True if the time given is in the correct specifed range.
        """
        menu = DailyMenu.objects.get(name="Test Menu")

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T14:00:00")
        self.assertIs(menu.check_available(test_time), True)

    def test_menu_check_availability_correct_daily_time_boundary(self):
        """
        Menu.check_availability(time) should return True if the time given is in the correct specifed range.
        The bounds should be inclusive.
        """
        menu = DailyMenu.objects.get(name="Test Menu")

        # Extreme upper bound
        test_time =  datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        self.assertIs(menu.check_available(test_time), True)

        # Extreme lower bound
        test_time =  datetime.datetime.fromisoformat("2020-01-01T16:00:00")
        self.assertIs(menu.check_available(test_time), True)

    def test_menu_check_availability_correct_daily_time_upper_bound(self):
        """
        Menu.check_availability(time) should return True if the time given is in the correct specifed range.
        """
        menu = DailyMenu.objects.get(name="Test Menu")       

        test_time =  datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        self.assertIs(menu.check_available(test_time), True)

    def test_menu_check_availability_before_daily_time(self):
        """
        Menu.check_availability(time) should return False is the given time is before the daily start. 
        """
        menu = DailyMenu.objects.get(name="Test Menu")

        test_time =  datetime.datetime.fromisoformat("2020-01-01T07:59:59")
        self.assertIs(menu.check_available(test_time), False)

    def test_menu_check_availability_after_daily_time(self):
        """
        Menu.check_availability(time) should return False is the given time is after the daily end. 
        """
        menu = DailyMenu.objects.get(name="Test Menu")

        test_time =  datetime.datetime.fromisoformat("2020-01-01T16:00:01")
        self.assertIs(menu.check_available(test_time), False)

    def test_menu_check_availability_after_daily_time(self):
        """
        Menu.check_availability(time) should return False is the given time is after the daily end. 
        """
        menu = DailyMenu.objects.get(name="Test Menu")

        test_time =  datetime.datetime.fromisoformat("2020-01-01T16:00:01")
        self.assertIs(menu.check_available(test_time), False)
        

