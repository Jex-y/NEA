import datetime

import django
from django.test import TestCase
from django.utils import timezone
from backend.models import Menu

class MenuModelTests(TestCase):

    def setUp(self):
        Menu.objects.create(name="Test Menu")

    def test_menu_check_availibility(self):
        """
        By default a menu should be available unless changed.
        """
        menu = Menu.objects.get(name="Test Menu")

        self.assertIs(menu.check_available(), True)

        menu.available=False
        menu.save()

        self.assertIs(menu.check_available(), False)

class DailyMenuModelTests(TestCase):

    def setUp(self):
        start_time = datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        end_time = datetime.datetime.fromisoformat("2020-01-01T16:00:00")
        Menu.objects.create(name="Test Menu", start_time=start_time, end_time=end_time)

    def test_menu_check_availability_correct_daily_time(self):
        """
        Menu.check_availability(time) should return True if the time given is in the correct specifed range.
        The bounds should be inclusive.
        """
        menu = Menu.objects.get(name="Test Menu")

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T14:00:00")
        self.assertIs(menu.check_available(test_time), True)

        # Extreme upper bound
        test_time =  datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        self.assertIs(menu.check_available(test_time), True)

        # Extreme lower bound
        test_time =  datetime.datetime.fromisoformat("2020-01-01T16:00:00")
        self.assertIs(menu.check_available(test_time), True)        

    def test_menu_check_availability_incorrect_daily_time(self):
        """
        Menu.check_availability(time) should return False is the given time is before the daily start or after the daily end. 
        """
        menu = Menu.objects.get(name="Test Menu")

        ## Before

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T07:00:00")
        self.assertIs(menu.check_available(test_time), False)

        # Extreme value 
        test_time =  datetime.datetime.fromisoformat("2020-01-01T07:59:59")
        self.assertIs(menu.check_available(test_time), False)

        ## After 

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T17:00:00")
        self.assertIs(menu.check_available(test_time), False)

        # Extreme value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T16:00:01")
        self.assertIs(menu.check_available(test_time), False)

class WeeklyMenuModelTestsNoTime(TestCase):

    def setUp(self):
        start_day = 0 # Monday
        end_day = 4 # Friday
        Menu.objects.create(name="Test Menu", start_day=start_day, end_day=end_day)

    def test_menu_check_availability_day_correct(self):
        """
        Menu.check_availability(time) should return True if the weekday is correct, no matter the time.
        """
        menu = Menu.objects.get(name="Test Menu")

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T12:00:00") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), True)

        # Extreme lower bound day 
        test_time =  datetime.datetime.fromisoformat("2020-01-06T12:00:00") # Monday, weekday no 0
        self.assertIs(menu.check_available(test_time), True)

        # Extreme upper bound day 
        test_time =  datetime.datetime.fromisoformat("2020-01-03T12:00:00") # Friday, weekday no 4
        self.assertIs(menu.check_available(test_time), True)

        # Extreme lower bound time
        test_time =  datetime.datetime.fromisoformat("2020-01-06T00:00:00") # Monday, weekday no 0
        self.assertIs(menu.check_available(test_time), True)

        # Extreme upper bound time
        test_time =  datetime.datetime.fromisoformat("2020-01-03T23:59:59") # Friday, weekday no 4
        self.assertIs(menu.check_available(test_time), True)

    def test_menu_check_availability_day_incorrect(self):
        """
        Menu.check_availability(time) should return False if the weekday is incorrect.
        """
        menu = Menu.objects.get(name="Test Menu")

        # Extreme lower bound
        test_time =  datetime.datetime.fromisoformat("2020-01-04T00:00:00") # Saturday, weekday no 5
        self.assertIs(menu.check_available(test_time), False)

        # Extreme upper bound
        test_time =  datetime.datetime.fromisoformat("2020-01-05T23:59:59") # Sunday, weekday no 6
        self.assertIs(menu.check_available(test_time), False)

class WeeklyMenuModelTestsWithTime(TestCase):

    def setUp(self):
        start_day = 0 # Monday
        end_day = 4 # Friday
        start_time = datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        end_time = datetime.datetime.fromisoformat("2020-01-01T16:00:00")
        Menu.objects.create(name="Test Menu", start_day=start_day, end_day=end_day, start_time=start_time, end_time=end_time)

    def test_menu_check_availability_correct_daily_time(self):
        """
        Menu.check_availability(time) should return True if the time given is in the correct specifed range.
        The bounds should be inclusive.
        """
        menu = Menu.objects.get(name="Test Menu")

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T14:00:00") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), True)

        # Extreme upper bound
        test_time =  datetime.datetime.fromisoformat("2020-01-01T08:00:00") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), True)

        # Extreme lower bound
        test_time =  datetime.datetime.fromisoformat("2020-01-01T16:00:00") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), True)        

    def test_menu_check_availability_incorrect_daily_time(self):
        """
        Menu.check_availability(time) should return False is the given time is before the daily start or after the daily end. 
        """
        menu = Menu.objects.get(name="Test Menu")

        ## Before

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T07:00:00") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), False)

        # Extreme value 
        test_time =  datetime.datetime.fromisoformat("2020-01-01T07:59:59") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), False)

        ## After 

        # Normal value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T17:00:00") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), False)

        # Extreme value
        test_time =  datetime.datetime.fromisoformat("2020-01-01T16:00:01") # Wednesday, weekday no 2
        self.assertIs(menu.check_available(test_time), False)

class MenuQueryTests(TestCase):
    def setUp(self):
        self.normal_menu1 = Menu.objects.create(name="Normal Menu 1")
        self.normal_menu2 = Menu.objects.create(name="Normal Menu 2", available=False)

        start_day = 0 # Monday
        end_day = 4 # Friday
        start_time = datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        end_time = datetime.datetime.fromisoformat("2020-01-01T16:00:00")

        self.weekly_menu1 = Menu.objects.create(name="Weekly Menu 1", start_day=start_day, end_day=end_day, start_time=start_time, end_time=end_time)

        start_day = 5 # Saturday
        end_day = 6 # Sunday

        self.weekly_menu2 = Menu.objects.create(name="Weekly Menu 2", start_day=start_day, end_day=end_day, start_time=start_time, end_time=end_time)

        self.daily_menu1 = Menu.objects.create(name="Daily Menu 1", start_time=start_time, end_time=end_time)

        start_time = datetime.datetime.fromisoformat("2020-01-01T16:00:00")
        end_time = datetime.datetime.fromisoformat("2020-01-01T20:00:00")

        self.daily_menu2 = Menu.objects.create(name="Daily Menu 2", start_time=start_time, end_time=end_time)

    def test_normal_available(self):
        test_time = datetime.datetime.fromisoformat("2020-01-01T12:00:00")
        queryset = Menu.objects.available(test_time)
        pks = [menu.pk for menu in queryset]
        
        self.assertEqual(self.normal_menu1.pk in pks, True)
        self.assertEqual(self.normal_menu2.pk in pks, False)

    def test_weekly_available(self):
        test_time = datetime.datetime.fromisoformat("2020-01-01T12:00:00") # Wednesday, weekday no 2
        queryset = Menu.objects.available(test_time)
        pks = [menu.pk for menu in queryset]
        
        self.assertEqual(self.weekly_menu1.pk in pks, True)
        self.assertEqual(self.weekly_menu2.pk in pks, False)

