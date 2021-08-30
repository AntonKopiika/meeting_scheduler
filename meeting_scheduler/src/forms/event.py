from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    start_date = DateField("Start date", validators=[DataRequired()])
    end_date = DateField("End date", validators=[DataRequired()])
    start_time = TimeField("From", validators=[DataRequired()])
    end_time = TimeField("To", validators=[DataRequired()])
    duration = IntegerField("Duration", validators=[DataRequired()])
    working_days = BooleanField("Working days")
    description = StringField("Description", validators=[DataRequired()])
    event_type = StringField("Event type", validators=[DataRequired()])
    submit = SubmitField("Create")
