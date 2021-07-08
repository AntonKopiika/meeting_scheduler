from src import db
from .models import User, Meeting
from src import bcrypt

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
            update_json["password"] = bcrypt.generate_password_hash(update_json["password"]).decode("utf-8")
        elif isinstance(instance, Meeting):
            instance.participants = update_json["participants"]
            update_json.pop("participants")
        db.session.query(self.cls).filter_by(id=instance.id).update(update_json)

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
