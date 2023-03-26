"""forum123's forms module."""

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):  # type: ignore
    """A class for a topic creation form."""

    title = TextAreaField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create topic")


class PostForm(FlaskForm):  # type: ignore
    """A class for a post creation form."""

    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Create post")
