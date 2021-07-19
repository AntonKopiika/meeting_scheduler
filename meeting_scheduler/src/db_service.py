from typing import List, Type, Union

from flask_sqlalchemy import SQLAlchemy

from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import Meeting, Timeslot, User

bcrypt = app_factory.get_bcrypt()


class CRUDService:
    def __init__(
            self,
            model: Type[Union[User, Meeting, Timeslot]],
            db: SQLAlchemy
    ):
        self.model = model
        self.db = db

    def add(self, instance: Union[User, Meeting, Timeslot]):
        self.db.session.add(instance)
        self.db.session.commit()

    def get(self, id: int) -> Union[User, Meeting, Timeslot]:
        return self.model.query.get(id)

    def get_all(self) -> List[Union[User, Meeting, Timeslot]]:
        return self.model.query.all()

    def update(
            self,
            instance: Union[User, Meeting, Timeslot],
            update_json: dict
    ):
        if isinstance(instance, User):
            update_json["password"] = bcrypt.\
                generate_password_hash(update_json["password"]).\
                decode("utf-8")
            self.model.query.filter_by(id=instance.id).update(update_json)
        elif isinstance(instance, Meeting):
            instance.participants = update_json["participants"]
            update_json.pop("participants")
            self.model.query.filter_by(id=instance.id).update(update_json)
        elif isinstance(instance, Timeslot):
            instance.start_time = update_json["start_time"]
            instance.end_time = update_json["end_time"]
            instance.user_id = update_json["user"]
            self.db.session.add(instance)
        self.db.session.commit()

    def delete(self, instance: Union[User, Meeting, Timeslot]):
        self.db.session.delete(instance)
        self.db.session.commit()
