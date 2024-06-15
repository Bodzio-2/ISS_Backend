from django.contrib import admin

from driveway_data.models import DrivewayEntry, ParkingSpot

# Register your models here.

admin.site.register(DrivewayEntry)
admin.site.register(ParkingSpot)