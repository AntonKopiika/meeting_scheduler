from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from meeting_scheduler.src import container, ServiceFactory
from meeting_scheduler.src.models import Timeslot
from meeting_scheduler.src.schemas.mixins import DeserializationMixin

db = ServiceFactory(container).get_db()


class TimeslotSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = Timeslot
        sqla_session = db.session
        include_relationships = True
        load_instance = True
