import injections
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


@injections.has
class AppContainer:
    app = injections.depends(Flask, "app")
    db = injections.depends(SQLAlchemy, "db")
    bcrypt = injections.depends(Bcrypt, "bcrypt")
    api = injections.depends(Api, "api")
