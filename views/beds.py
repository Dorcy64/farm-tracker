from flask import Blueprint, request
from lib.util_datetime import tzware_datetime, timedelta_days
from lib.util_requests import render_json, strip_tags_from_request
from models import Bed, Plant, CurrentPlant
from app import db

beds_blueprint = Blueprint('beds', __name__)


@beds_blueprint.route("/", methods=['GET', 'POST'])
@beds_blueprint.route('/view-all-beds', methods=["POST", "GET"])
def all_beds():
    beds = db.session.query(Bed).all()
    return render_json(200, [b.serialize for b in beds])


@beds_blueprint.route('/create-bed', methods=["POST"])
def create_bed():
    bed_id = request.args.get('bed_id', type=int)

    if bed_id is None or Bed.query.get(bed_id) is not None:
        return render_json(400, "'bed_id' cant be None, or is already created please send the bed id")

    new_bed = Bed(
        id=bed_id,
        bed_type=request.args.get('bed_type', type=str, default="field"),
    )
    new_bed.save()

    return render_json(201, new_bed.serialize)


@beds_blueprint.route('/view-bed/<int:bed_id>', methods=["POST", "GET"])
def view_bed(bed_id):
    if bed_id is None:
        return render_json(404, "Bed id can't be none or wasn't included in the url")

    bed_object = Bed.query.get(bed_id)
    if bed_object is None:
        return render_json(404, "Bed wasn't found consider creating a new bed instead")

    if len(bed_object.current_plant) > 1:
        previous_plants = []
        for plantations in bed_object.current_plant:
            if plantations != bed_object.current_plant[-1]:
                previous_plants.append({
                    "plant_id": plantations.plant_id,
                    "plant_name": plantations.plant_title(),
                    "planted_date": plantations.planted_date,
                    "harvest_date": plantations.harvest_start_date,
                    "notes": plantations.notes,
                })
        serialized_output = bed_object.serialize
        serialized_output["previous_plants"] = previous_plants
        return render_json(200, serialized_output)

    return render_json(200, bed_object.serialize)


@beds_blueprint.route('/edit-bed', methods=["POST"])
def edit_bed():
    bed_id = request.args.get('bed_id', type=int)
    if bed_id is None:
        return render_json(404, "'bed_id' cant be None, or is already created please send the bed id")

    bed_object = Bed.query.get(bed_id)
    if bed_object is None:
        return render_json(404, "Consider creating the bed, because it wasn't found or is missing")

    bed_type = request.args.get('bed_type', type=str)
    if bed_type is not None:
        bed_object.bed_type = bed_type

    if len(bed_object.current_plant) > 0:
        current_plant = CurrentPlant.query.get(bed_object.current_plant[-1].id)

        plant_id = request.args.get('plant_id', type=int)
        if plant_id is not None:
            current_plant.plant_id = plant_id

        days_ago_planted = request.args.get('days_ago_planted', type=int)
        if days_ago_planted is not None:
            days_ago_planted = -abs(days_ago_planted)
            current_plant.change_dates(days_ago_planted)

        notes = request.args.get('notes', type=str)
        if notes is not None:
            current_plant.notes = notes

        current_plant.save()

    bed_object.save()

    return render_json(201, bed_object.serialize)


@beds_blueprint.route('/delete-bed', methods=["POST"])
def delete_bed():
    bed_id = request.args.get('bed_id', type=int)
    if bed_id is None:
        return render_json(404, "Make sure to include the bed_id in the request")

    bed_object = Bed.query.get(bed_id)
    if bed_object is None:
        return render_json(400, "The bed has already been deleted or is missing")

    bed_object.delete()
    return render_json(200, "The bed was successfully deleted")


@beds_blueprint.route('/clear-bed', methods=["POST"])
def clear_bed():
    bed_id = request.args.get('bed_id', type=int)
    if bed_id is None:
        return render_json(404, "Make sure to include the bed_id in the request")

    bed_object = Bed.query.get(bed_id)
    if bed_object is None:
        return render_json(400, "The bed has already been deleted or is missing")

    bed_type = bed_object.bed_type
    bed_object.delete()

    new_bed = Bed(
        id=bed_id,
        bed_type=bed_type,
    )
    new_bed.save()
    return render_json(200, new_bed.serialize)
