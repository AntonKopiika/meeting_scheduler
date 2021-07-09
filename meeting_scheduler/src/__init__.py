import injections
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from container import DBConnection

app = Flask(__name__)
container = injections.Container()
container["db"] = SQLAlchemy(app)
container["bcrypt"] = Bcrypt(app)
container["api"] = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class DBFactory:
    def __init__(self):
        self.db_conn = container.inject(DBConnection())

    def get_db(self):
        return self.db_conn.db

    def get_bcrypt(self):
        return self.db_conn.bcrypt

    def get_api(self):
        return self.db_conn.api


from .rest import routes
