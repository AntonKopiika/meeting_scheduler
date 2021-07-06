from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/flask_test'
db = SQLAlchemy(app)
api = Api(app)

from rest import routes

if __name__ == '__main__':
    app.run()
