from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Email


class MeetingForm(FlaskForm):
    start_time = DateTimeField("Start time", validators=[DataRequired()])
    attendee_name = StringField("Your name", validators=[DataRequired()])
    attendee_email = StringField("Email", validators=[DataRequired(), Email()])
    link = StringField("Link", validators=[DataRequired()])
    additional_info = StringField("Additional info", validators=[DataRequired()])
    submit = SubmitField("Create")
