from flask import Blueprint, request
from lib.util_datetime import tzware_datetime, timedelta_days
from lib.util_requests import render_json, strip_tags_from_request
from models import Bed, Plant, CurrentPlant
from app import db

current_plants = Blueprint('api', __name__)


@current_plants.route('/plant-bed', methods=["POST"])
def plant_bed():
    bed_id = request.args.get('bed_id', type=int)
    plant_id = request.args.get('plant_id', type=int)
    if bed_id is None or plant_id is None:
        return render_json(400, "'bed_id' Can't be None | Send the request with the bed you want to plant on")

    bed_object = Bed.query.get(bed_id)
    plant_object = Plant.query.get(plant_id)
    if bed_object is None or bed_object.is_bed_occupied():
        return render_json(400, "You can't plant new plants on a bed that's already occupied or missing")
    if plant_object is None:
        return render_json(400, "Plant not found or is not yet created")

    new_current_plant = CurrentPlant(
        planted_date=tzware_datetime(),
        harvest_start_date=timedelta_days(plant_object.days_to_grow),
        harvest_end_date=timedelta_days((plant_object.days_to_grow + plant_object.days_to_harvest)),
        notes=request.args.get('notes', type=str),
        bed_id=bed_id,
        plant_id=plant_id,
    )
    new_current_plant.save()

    return render_json(201, bed_object.serialize)


@current_plants.route('/delete-current-plant', methods=["POST"])
def delete_current_plant():
    current_plant = request.args.get('current_plant_id', type=int)
    if current_plant is None:
        return render_json(400, "Make sure to include the 'current_plant_id' in the request")

    current_plant_object = CurrentPlant.query.get(current_plant)
    if current_plant_object is None:
        return render_json(400, "The current plant was not found consider checking the bed instead")

    current_plant_object.delete()
    return render_json(200, "The 'current_plant' was successfully deleted")


@current_plants.route('/current-plant-status', methods=["POST", "GET"])
def change_current_plant_status():
    current_plant_id = request.args.get('current_plant_id', type=int)
    if current_plant_id is None:
        return render_json(400, "'current_plant_id' cant be None, or is missing")

    current_plant = CurrentPlant.query.get(current_plant_id)
    if current_plant is None:
        return render_json(400, "Current plant is not found, or has been deleted, consider checking the bed")

    if request.method == "POST":
        change_plant_status = request.args.get('change_plant_status', type=bool)
        if change_plant_status is not None:
            current_plant.change_status()

    return render_json(200, current_plant.bed.serialize)
