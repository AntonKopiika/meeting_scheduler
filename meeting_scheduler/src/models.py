from datetime import datetime
from typing import List
from meeting_scheduler.src import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    timeslots = db.relationship('Timeslot', backref='user', lazy=True)
    meetings = db.relationship('Meeting', backref='host', lazy=True)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'<User: {self.username}>'

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, start_time: datetime, end_time: datetime, user: User):
        self.start_time = start_time
        self.end_time = end_time
        self.user = user
        self.user_id = user.id

    def __repr__(self):
        return f'<Timeslot: {self.start_time}-{self.end_time} for {self.user}>'


participants = db.Table(
    'participant',
    db.Column('participant_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meeting_start_time = db.Column(db.DateTime, nullable=False)
    meeting_end_time = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(32), nullable=False)
    comment = db.Column(db.String(256))
    link = db.Column(db.String(64), nullable=False)
    details = db.Column(db.String(64), nullable=False)
    participants = db.relationship('User', secondary=participants, lazy='subquery',
                                   backref=db.backref('invitations', lazy=True))

    def __init__(
            self,
            host: User,
            participants: List[User],
            meeting_start_time: datetime,
            host_id: int,
            meeting_end_time: datetime,
            title: str,
            details: str,
            link: str,
            comment: str = None
    ):
        self.host_id = host_id
        self.host = host
        self.meeting_start_time = meeting_start_time
        self.meeting_end_time = meeting_end_time
        self.title = title
        self.details = details
        self.link = link
        self.comment = comment
        self.participants = participants

    def __repr__(self):
        return f'<Meeting: {self.meeting_start_time}-{self.meeting_start_time} for {self.host}>'
