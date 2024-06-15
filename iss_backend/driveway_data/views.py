from django.shortcuts import render
from json import load, loads, dumps

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
        
class DrivewayEntryView:

    @add_http_options
    class Get(View):
        http_method_names = ['get']

        @staticmethod
        def get(request, spot_id) -> JsonResponse:
            # Returns a list of all entries for that spot
            try:
                parking_spot = ParkingSpot.objects.get(id=spot_id)
            except ObjectDoesNotExist as error:
                return JsonResponse({
                        "error": "Parking Spot with specified id wasn't found!",
                        "details": str(error),
                        "error_data": {
                            "id_not_found": spot_id,
                        },
                    }, status=404)

            try:
                entries = []

                for entry in DrivewayEntry.objects.all():
                    if entry.parking_spot == parking_spot:
                        entries.append(view_utils.get_fields(entry))
                # dumps(entries, indent=4, sort_keys=True, default=str),
                return JsonResponse({
                    "entry_count": len(entries),
                    "entries": entries,
                    }, status=200)
            except Exception as error:
                return JsonResponse({
                    "error" : "an unexpected exception occured!",
                    "details" : str(error)
                }, status=500)

    @add_http_options
    class Post(View):
        http_method_names = ['post']

        @staticmethod
        def post(request, spot_id) -> JsonResponse:
            # Adds a new entry to a given spot
            json_data = loads(request.body)

            data_ser = DrivewayEntrySerializer(data=json_data)

            if data_ser.is_valid():
                try:
                    new_entry = view_utils.create_driveway_entry(json_data, spot_id)
                    return JsonResponse({"driveway_entry" : {"id": new_entry.id, "data" : {**json_data}}}, status=201)
                except Exception as e:
                    return JsonResponse({"error": "Internal server error: " + str(e)}, status = 401)
            else:
                return JsonResponse({"error": "Invalid data!"}, status=401)
    
    @add_http_options
    class Delete(View):
        http_method_names = ['delete']

        @staticmethod
        def delete(request, spot_id) -> JsonResponse:
            # Deletes all entries from given spot
            try:
                parking_spot = ParkingSpot.objects.get(id=spot_id)
            except ObjectDoesNotExist as error:
                return JsonResponse({
                        "error": "Parking Spot with specified id wasn't found!",
                        "details": str(error),
                        "error_data": {
                            "id_not_found": spot_id,
                        },
                    }, status=404)
            
            entries = DrivewayEntry.objects.filter(parking_spot = parking_spot)

            i = 0

            for entry in entries:
                i+=1
                entry.delete()

            return JsonResponse({
                "message": "success",
                "entries removed" : i,
            }, status = 200)
    
class SpecificEntryView:

    @add_http_options
    class Get(View):
        http_method_name = ['get']

        @staticmethod
        def get(request, entry_id) -> JsonResponse:
            # get an entry of a specific ID
            try:
                driveway_entry = view_utils.get_driveway_entry(entry_id)
                return JsonResponse({driveway_entry}, status=200)
            except ObjectDoesNotExist as error:
                return JsonResponse({
                    "error": "Driveway entry with specified id wasn't found!",
                    "details": str(error),
                    "error_data": {
                        "id_not_found": entry_id,
                    },
                }, status=404)
    
    @add_http_options
    class Delete(View):
        http_method_names = ['delete']


        @staticmethod
        def delete(request, entry_id) -> JsonResponse:
            # delete a specific entry
            try:
                DrivewayEntry.objects.delete(entry_id)
            except ObjectDoesNotExist as error:
                return JsonResponse({
                    "error": "Driveway entry with specified id wasn't found!",
                    "details": str(error),
                    "error_data": {
                        "id_not_found": entry_id,
                    },
                }, status=404)
            
            return JsonResponse({"deleted_id" : entry_id}, status=200)