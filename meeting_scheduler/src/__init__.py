import os

import injections
from containers import AppContainer
from flask import Flask
from flask_restful import Api

from meeting_scheduler.src.models import bcrypt, db


def create_app_container(db_uri):
    container = injections.Container()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bcrypt.init_app(app)
    api = Api(app)
    if app.app_context() is None:
        app.app_context().pop()
    app.app_context().push()
    if db_uri == "sqlite:///:memory:":
        db.create_all()
    container["app"] = app
    container["db"] = db
    container["bcrypt"] = bcrypt
    container["api"] = api
    return container


class AppFactory:
    def set_container(self, test_service=False):
        if test_service:
            test_container = create_app_container("sqlite:///:memory:")
            self.container = test_container.inject(AppContainer())
        else:
            container = create_app_container(os.environ.get("DATABASE_URI"))
            self.container = container.inject(AppContainer())

    def get_app(self):
        return self.container.app

    def get_db(self):
        return self.container.db

    def get_bcrypt(self):
        return self.container.bcrypt

    def get_api(self):
        return self.container.api


app_factory = AppFactory()
app_factory.set_container(test_service=True)

from .rest import routes
