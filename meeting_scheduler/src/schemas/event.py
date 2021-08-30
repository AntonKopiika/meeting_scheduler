from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import Event
from meeting_scheduler.src.schemas.mixins import DeserializationMixin

db = app_factory.get_db()


class EventSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = Event
        sqla_session = db.session
        include_relationships = True
        load_instance = True
