from django.db import models
from django.utils import timezone

class MenuManager(models.Manager):
    
    def available(self, time=timezone.now()):
        return [ menu for menu in super(MenuManager, self).all() if menu.check_available(time) ]