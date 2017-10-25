from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class EmailForm(FlaskForm):
    """ Form used to submit messages to the admin. """
    name = StringField('Name')
    reply_to = StringField('Email', validators=[Email(), DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')