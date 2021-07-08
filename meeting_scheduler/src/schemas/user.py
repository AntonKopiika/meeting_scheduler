from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from meeting_scheduler.src.models import User
from meeting_scheduler.src.schemas.mixins import DeserializationMixin


class UserSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
