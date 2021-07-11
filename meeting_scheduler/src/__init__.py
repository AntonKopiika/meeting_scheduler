import injections
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from container import ServiceContainer, AppContainer


def create_service_container(app):
    container = injections.Container()
    container["db"] = SQLAlchemy(app)
    container["bcrypt"] = Bcrypt(app)
    container["api"] = Api(app)
    return container


def create_app():
    container = injections.Container()
    container["app"] = Flask(__name__)
    app = container.inject(AppContainer()).app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


app = create_app()
container = create_service_container(app)


class ServiceFactory:
    def __init__(self, container):
        self.con = container.inject(ServiceContainer())

    def get_db(self):
        return self.con.db

    def get_bcrypt(self):
        return self.con.bcrypt

    def get_api(self):
        return self.con.api


from .rest import routes
