from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from meeting_scheduler.src.models import Timeslot
from meeting_scheduler.src.schemas.mixins import DeserializationMixin


class TimeslotSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = Timeslot
        include_relationships = True
        load_instance = True
