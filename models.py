from sqlalchemy.orm import relationship
from collections import OrderedDict
from lib.util_sqlalchemy import AwareDateTime, ResourceMixin
from lib.util_datetime import timedelta_days
from app import db


class Bed(db.Model, ResourceMixin):
    __tablename__ = "beds"
    BED_TYPE = OrderedDict([("raised", "Raised"), ("field", "Field"), ("container", "Container")])

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bed_type = db.Column(
        db.Enum(*BED_TYPE, name="bed_type", native_enum=False),
        index=True,
        nullable=False,
        server_default="field",
    )
    current_plant = relationship("CurrentPlant", back_populates="bed", cascade="all, delete-orphan")

    def status(self):
        if len(self.current_plant) == 0:
            return "empty"
        return self.current_plant[-1].status

    def is_bed_occupied(self):
        current_status = self.status()
        if current_status == "empty" or current_status == "harvested":
            return False
        return True

    @property
    def serialize(self):
        if len(self.current_plant) == 0:
            return {
                "id": self.id,
                "type": self.bed_type,
                "status": self.status()
            }
        return {
            "bed_id": self.id,
            "bed_type": self.bed_type,
            "plant_id": self.current_plant[-1].plant_id,
            "plant_name": self.current_plant[-1].plant_title(),
            "current_plant_id": self.current_plant[-1].id,
            "planted_date": self.current_plant[-1].planted_date,
            "harvest_date": self.current_plant[-1].harvest_start_date,
            "notes": self.current_plant[-1].notes,
            "status": self.status(),
        }


class Plant(db.Model, ResourceMixin):
    __tablename__ = "plants"
    PLANT_TYPE = OrderedDict([("herb", "Herb"), ("flowers", "Flowers"), ("veggie", "Veggie"), ("fruit", "Fruit")])

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    good_combos = db.Column(db.Text)
    bad_combos = db.Column(db.Text)
    days_to_grow = db.Column(db.Integer, nullable=False)
    days_to_harvest = db.Column(db.Integer, nullable=False)
    plant_type = db.Column(
        db.Enum(*PLANT_TYPE, name="plant_type", native_enum=False),
        index=True,
        nullable=False,
        server_default="veggie",
    )
    current_plant = relationship("CurrentPlant", back_populates="plant", cascade="all, delete-orphan")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "good_combos": self.good_combos,
            "bad_combos": self.bad_combos,
            "days_to_grow": self.days_to_grow,
            "days_to_harvest": self.days_to_harvest,
            "type": self.plant_type,
        }


class CurrentPlant(db.Model, ResourceMixin):
    __tablename__ = "current_plants"

    STATUS = OrderedDict([("planted", "Planted"), ("harvested", "Harvested")])

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    planted_date = db.Column(AwareDateTime(), nullable=False)
    harvest_start_date = db.Column(AwareDateTime(), nullable=True)
    harvest_end_date = db.Column(AwareDateTime(), nullable=True)

    status = db.Column(
        db.Enum(*STATUS, name="plant_status", native_enum=False),
        index=True,
        nullable=False,
        server_default="planted",
    )

    notes = db.Column(db.Text)

    bed_id = db.Column(db.String, db.ForeignKey("beds.id"))
    bed = relationship("Bed", back_populates="current_plant")

    plant_id = db.Column(db.String, db.ForeignKey("plants.id"))
    plant = relationship("Plant", back_populates="current_plant")

    def plant_title(self):
        if self.plant is not None:
            return self.plant.title
        return None

    def change_dates(self, days):
        self.planted_date = timedelta_days(days, self.planted_date)
        self.harvest_start_date = timedelta_days(days, self.harvest_start_date)
        self.harvest_end_date = timedelta_days(days, self.harvest_end_date)
        self.save()

    def change_status(self):
        if self.status == "planted":
            self.status = "harvested"
            return self.save()
        else:
            self.status = "planted"
            return self.save()


db.create_all()
