from rest_framework import serializers
from driveway_data.models import ParkingSpot
from driveway_data.models import DrivewayEntry

class ParkingSpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpot
        fields = ['tags']
        depth = 3


class DrivewayEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivewayEntry
        fields = ['parking_spot', 'timestamp', 'action']
        depth = 3
