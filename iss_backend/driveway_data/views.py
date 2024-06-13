from django.shortcuts import render
from json import load, loads

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from .models import *
import utils.view_utils as view_utils
from utils.http_options_decorator import add_http_options
from utils.data_serializer import ParkingSpotSerializer
from utils.data_serializer import DrivewayEntrySerializer

# Create your views here.


class ParkingSpotView:
    @add_http_options
    class GetId(View):
        http_method_names = ['get']

        @staticmethod
        def get(request, spot_id: int) -> JsonResponse:
            try:
                parking_spot = view_utils.get_parking_spot(spot_id)

                return JsonResponse({"parking_spot" : parking_spot}, status=200)
            except ObjectDoesNotExist as error:
                return JsonResponse({
                    "error": "Parking Spot with specified id wasn't found!",
                    "details": str(error),
                    "error_data": {
                        "id_not_found": spot_id,
                    },
                }, status=404)
    @add_http_options
    class Post(View):
        http_method_names = ['post']

        @staticmethod
        def post(request) -> JsonResponse:
            json_data = loads(request.body)

            data_ser = ParkingSpotSerializer(data=json_data)

            if data_ser.is_valid():
                try:
                    new_parking_spot = view_utils.create_parking_spot(json_data)
                    return JsonResponse({"parking_spot" : {"id": new_parking_spot.id, "data": {**json_data}}}, status=201)
                except Exception as e:
                    print("An unexpected Exception occured: ", str(e))
            else:
                return JsonResponse({"error": "Provided parking spot data is invalid!"}, status=400)
            
class ParkingSpotActionsView:
    @add_http_options
    class GetActionEnum(View):
        http_method_names = ['get']

        @staticmethod
        def get(request) -> JsonResponse:
            return JsonResponse({a:a.value for a in DrivewayEntry.Action}, status=200)
        
@add_http_options
class DrivewayEntryView:
    http_method_names = ['get', 'post', 'delete']

    @staticmethod
    def get(request, spot_id) -> JsonResponse:
        # Returns a list of all entries for that spot
        
        pass

    @staticmethod
    def post(request, spot_id) -> JsonResponse:
        # Adds a new entry to a given spot
        json_data = loads(request.body)

        data_ser = DrivewayEntrySerializer(data=json_data)

        if data_ser.is_valid():
            try:
                new_entry = view_utils.create_driveway_entry(json_data)
                return JsonResponse({"driveway_entry" : {"id": new_entry.id, "data" : {**json_data}}}, status=201)
            except Exception as e:
                return JsonResponse({"error": "Internal server error: " + str(e)}, status = 500)
        else:
            return JsonResponse({})
    @staticmethod
    def delete(request, spot_id) -> JsonResponse:
        # Deletes all entries from given spot
        pass
    
    @add_http_options
    class SpecificEntry:
        http_method_names = ['get, delete']

        def get(request, entry_id) -> JsonResponse:
            # get an entry of a specific ID
            pass

        def delete(request, entry_id) -> JsonResponse:
            # delete a specific entry
            pass