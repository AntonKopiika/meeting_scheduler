import injections
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


@injections.has
class DBConnection:
    db = injections.depends(SQLAlchemy, "db")
    bcrypt = injections.depends(Bcrypt, "bcrypt")
    api = injections.depends(Api, "api")

