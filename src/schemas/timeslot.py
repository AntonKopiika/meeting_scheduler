from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models import Timeslot
from src.schemas.mixins import DeserializationMixin


class TimeslotSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = Timeslot
        include_relationships = True
        load_instance = True
