from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from meeting_scheduler.src import ServiceFactory, container
from meeting_scheduler.src.models import Meeting
from meeting_scheduler.src.schemas.mixins import DeserializationMixin

db = ServiceFactory(container).get_db()


class MeetingSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = Meeting
        sqla_session = db.session
        include_relationships = True
        include_fk = True
        load_instance = True
