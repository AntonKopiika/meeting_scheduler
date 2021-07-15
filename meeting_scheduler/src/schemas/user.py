from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import User
from meeting_scheduler.src.schemas.mixins import DeserializationMixin

db = app_factory.get_db()


class UserSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = User
        sqla_session = db.session
        include_relationships = True
        load_instance = True
