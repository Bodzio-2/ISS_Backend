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