from enum import Enum
from django.db import models

# Create your models here.

class ParkingSpot(models.Model):
    tags = models.CharField(max_length=100)

class DrivewayEntry(models.Model):
    class Action(str, Enum):
        Take = 'Take'
        Free = 'Free'

    parking_spot = models.ForeignKey('ParkingSpot')
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=100)
