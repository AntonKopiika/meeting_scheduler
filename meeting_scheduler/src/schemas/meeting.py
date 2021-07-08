from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from meeting_scheduler.src.models import Meeting
from meeting_scheduler.src.schemas.mixins import DeserializationMixin


class MeetingSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = Meeting
        include_relationships = True
        include_fk = True
        load_instance = True
