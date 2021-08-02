from marshmallow import ValidationError

from meeting_scheduler.src import app_factory

db = app_factory.get_db()


class DeserializationMixin:
    def deserialize(self, json: dict):
        instance = None
        try:
            instance = self.load(json)
            db.session.rollback()
        except ValidationError as err:
            # TODO: make logging error
            print({"message": str(err)})
        return instance
