
from django.conf import settings
from django.db import models


class Day(models.Model):
    day  = models.CharField(max_length=settings.MAX_CAPACITY)
    max_capacity = models.IntegerField(default=8)

class Booking(models.Model):
    user = models.CharField(max_length=32)
    day  = models.CharField(max_length=8)
    
class Department(models.Model):
    user = models.CharField(max_length=32)
    department_name = models.CharField(max_length=32)
