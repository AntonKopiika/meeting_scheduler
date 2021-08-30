from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    events = db.relationship(
        'Event',
        backref='host',
        lazy=True,
        cascade="all, delete"
    )
    meetings = db.relationship(
        'Meeting',
        backref='host',
        lazy=True,
        cascade="all, delete"
    )
    accounts = db.relationship(
        'UserAccount',
        backref='user',
        lazy=True,
        cascade="all, delete"
    )

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'<User: {self.username}>'

    def check_password(self, password: str):
        return bcrypt.check_password_hash(self.password, password)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    working_days = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(256))
    event_type = db.Column(db.String(256), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    meetings = db.relationship(
        'Meeting',
        backref='event',
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f'<Event: {self.start_time}-{self.end_time} for {self.host}>'


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    calendar_event_id = db.Column(db.String(256))
    attendee_name = db.Column(db.String(64))
    attendee_email = db.Column(db.String(64))
    link = db.Column(db.String(256), nullable=False)
    additional_info = db.Column(db.String(256))

    def __repr__(self):
        return f'<Meeting: {self.start_time} event: {self.event}, user: {self.host}>'


class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    cred = db.Column(db.LargeBinary(1024), nullable=False)
    provider = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<UserAccount: {self.email} for {self.user}>'
