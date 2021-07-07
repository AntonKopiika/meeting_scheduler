from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models import Meeting


class MeetingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Meeting
        include_relationships = True
        include_fk=True
        load_instance = True
