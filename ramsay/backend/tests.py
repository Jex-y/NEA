import datetime
import django
from django.test import TestCase
from django.utils import timezone
from .models import Menu


# TODO: Configure your database in settings.py and sync before running tests

class MenuModelTests(TestCase):

    def test_menu_check_availability_correct_time(self):
        """
        Menu.check_availability(time) should return True if the time given is in the correct specifed range.
        At all other times it should return False. 
        The time period should be able to reoccur either daily or weekly. 
        """
        start_time = datetime.datetime.fromisoformat("2020-01-01T08:00:00")
        end_time = datetime.datetime.fromisoformat("2020-01-01T16:00:00")
        test_time =  datetime.datetime.fromisoformat("2020-01-01T14:00:00")
        menu = Menu(name="Test Menu", start_time=start_time, end_time=end_time, reoccurs="DY")
        self.assertIs(menu.check_available(test_time), True)
        
