from flask import Blueprint, request
from lib.util_datetime import tzware_datetime, timedelta_days
from lib.util_requests import render_json, strip_tags_from_request
from models import Bed, Plant, CurrentPlant
from app import db
from sqlalchemy.exc import IntegrityError


plants = Blueprint('current_plants', __name__)


@plants.route('/view-all-plants', methods=["POST", "GET"])
def all_plants():
    plant = db.session.query(Plant).all()
    return render_json(200, [p.serialize for p in plant])


@plants.route('/create-plant', methods=["POST"])
def create_plant():
    title = request.args.get('title', type=str)
    days_to_grow = request.args.get('days_to_grow', type=int)
    days_to_harvest = request.args.get('days_to_harvest', type=int)

    if title is None or title == "" or days_to_grow is None or days_to_harvest is None:
        return render_json(400, "'new_bed_id' cant be None, or is already created please send the bed id")

    try:
        new_plant = Plant(
            title=title,
            good_combos=request.args.get("good_combos", type=str),
            bad_combos=request.args.get("bad_combos", type=str),
            plant_type=request.args.get('plant_type', type=str, default="veggie"),
            days_to_grow=days_to_grow,
            days_to_harvest=days_to_harvest,
        )
        new_plant.save()
    except IntegrityError:
        db.session.rollback()
        return render_json(400, "The plant title is already taken consider editing the plant instead")

    return render_json(201, new_plant.serialize)


@plants.route('/edit-plant', methods=["POST"])
def edit_plant():
    plant_id = request.args.get('plant_id', type=int)
    if plant_id is None:
        return render_json(404, "Plant not found Make sure to include the 'plant_id' in the request")

    plant_object = Plant.query.get(plant_id)
    if plant_object is None:
        return render_json(404, "The plant was not found consider retrieving a list of all plants")

    title = request.args.get('title', type=str)
    if title is not None:
        plant_object.title = title

    days_to_grow = request.args.get('days_to_grow', type=int)
    if days_to_grow is not None:
        plant_object.days_to_grow = days_to_grow

    days_to_harvest = request.args.get('days_to_harvest', type=int)
    if days_to_harvest is not None:
        plant_object.days_to_harvest = days_to_harvest

    plant_type = request.args.get('plant_type', type=str)
    if plant_type is not None:
        plant_object.plant_type = plant_type

    good_combos = request.args.get('good_combos', type=str)
    if good_combos is not None:
        plant_object.good_combos = good_combos

    bad_combos = request.args.get('bad_combos', type=str)
    if bad_combos is not None:
        plant_object.bad_combos = bad_combos

    plant_object.save()

    return render_json(200, "The 'current_plant' was successfully deleted")


@plants.route('/delete-plant', methods=["POST"])
def delete_plant():
    plant_id = request.args.get('plant_id', type=int)
    if plant_id is None:
        return render_json(404, "Make sure to include the 'plant_id' in the request")

    plant_object = Plant.query.get(plant_id)
    if plant_object is None:
        return render_json(404, "The plant was not found consider retrieving all the plants")

    plant_object.delete()
    return render_json(200, "The 'plant' was successfully deleted")
