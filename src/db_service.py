from src import db
from .models import User, Meeting, Timeslot
from werkzeug.security import generate_password_hash


class CRUDService:
    def __init__(self, cls):
        self.cls = cls

    def add(self, instance):
        db.session.add(instance)
        db.session.commit()

    def get(self, id):
        return self.cls.query.get(id)

    def get_all(self):
        return self.cls.query.all()

    def update(self, instance, update_json: dict):
        if isinstance(instance, User):
            update_json["password"] = generate_password_hash(update_json["password"])
        elif isinstance(instance, Meeting):
            instance.participants = update_json["participants"]
            update_json.pop("participants")
        db.session.query(self.cls).filter_by(id=instance.id).update(update_json)


    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
