from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models import Timeslot


class TimeslotSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Timeslot
        include_relationships = True
        load_instance = True
