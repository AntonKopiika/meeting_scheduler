from typing import Type, Union

from flask_sqlalchemy import SQLAlchemy

from meeting_scheduler.src.models import User, Meeting, Timeslot
from meeting_scheduler.src import ServiceFactory, container

factory = ServiceFactory(container)
bcrypt = factory.get_bcrypt()


class CRUDService:
    def __init__(self, model: Type[Union[User, Meeting, Timeslot]], db: SQLAlchemy):
        self.model = model
        self.db = db

    def add(self, instance: Union[User, Meeting, Timeslot]):
        self.db.session.add(instance)
        self.db.session.commit()

    def get(self, id: int):
        return self.model.query.get(id)

    def get_all(self):
        return self.model.query.all()

    def update(self, instance: Union[User, Meeting, Timeslot], update_json: dict):
        if isinstance(instance, User):
            update_json["password"] = bcrypt.generate_password_hash(update_json["password"]).decode("utf-8")
        elif isinstance(instance, Meeting):
            instance.participants = update_json["participants"]
            update_json.pop("participants")
        self.db.session.query(self.model).filter_by(id=instance.id).update(update_json)

    def delete(self, instance: Union[User, Meeting, Timeslot]):
        self.db.session.delete(instance)
        self.db.session.commit()
