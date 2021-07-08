from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models import User
from src.schemas.mixins import DeserializationMixin


class UserSchema(SQLAlchemyAutoSchema, DeserializationMixin):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
