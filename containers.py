import injections
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


@injections.has
class AppContainer:
    app = injections.depends(Flask, "app")
    db = injections.depends(SQLAlchemy, "db")
    bcrypt = injections.depends(Bcrypt, "bcrypt")
    api = injections.depends(Api, "api")


@injections.has
class TestContainer:
    a = injections.depends(int, "a")
