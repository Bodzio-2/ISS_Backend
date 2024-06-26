from driveway_data.models import *
from django.forms.models import model_to_dict
from django.db.models import Model


def get_fields(model: models.Model, fields: dict = None, ignore_models:list = []) -> dict:
    if not fields:
        fields = {}
        for f in model._meta.fields:
            fields[f.name] = getattr(model, f.name)

        for f in model._meta.many_to_many:
            fields[f.name] = get_many_to_many(getattr(model, f.name))

    for name, value in fields.items():
        if not isinstance(value, models.Model):
            # skip non-relational (ForeignKey) fields            
            continue
        fields[name] = getattr(value, "pk") if name in ignore_models else get_fields(value)
    return fields

def get_many_to_many(many_to_many) -> list:
    ret_list = []
    for val in many_to_many.all():
        ret_list.append(get_fields(val))
    return ret_list


def get_parking_spot(spot_id: int) -> dict:
    parking_spot = ParkingSpot.objects.get(id=spot_id)
    parking_spot_dict = get_fields(parking_spot)

    return parking_spot_dict

def create_parking_spot(json_data: dict) -> ParkingSpot:
    new_parking_spot = ParkingSpot.objects.create(**json_data)

    return new_parking_spot

def create_driveway_entry(json_data: dict, spot_id: int) -> DrivewayEntry:
    # TODO create helper function for creating a new driveway entry
    for parking_spot in ParkingSpot.objects.all():
        if spot_id == parking_spot.pk:
            new_entry = DrivewayEntry.objects.create(**json_data, parking_spot=parking_spot)
            return new_entry
    raise Exception("Parking spot with given ID was not found")
    



def get_driveway_entry(entry_id: int) -> dict:
    driveway_entry = DrivewayEntry.objects.get(id=entry_id)

    driveway_entry_dict = get_fields(driveway_entry)

    return driveway_entry_dict