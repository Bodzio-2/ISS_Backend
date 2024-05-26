from django.shortcuts import render
from json import load, loads

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from .models import *
import iss_backend.utils.view_utils as view_utils
from iss_backend.utils.http_options_decorator import add_http_options

# Create your views here.


class ParkingSpotView:
    @add_http_options
    class GetId(View):
        http_method_names = ['get', 'post']

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
        
        @staticmethod
        def post(request) -> JsonResponse:
            json_data = loads(request.body)

            