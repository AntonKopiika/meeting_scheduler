from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models import Meeting
from src.schemas.mixins import DeserializationMixin


class MeetingSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = Meeting
        include_relationships = True
        include_fk = True
        load_instance = True
