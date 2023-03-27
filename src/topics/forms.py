"""Forms module of 'topics' package."""

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):  # type: ignore
    """A class for a topic creation form."""

    title = TextAreaField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create topic")
