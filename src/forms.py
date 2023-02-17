"""forum123's forms module."""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):  # type: ignore
    """A class for a regitration form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):  # type: ignore
    """A class for a login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class TopicForm(FlaskForm):  # type: ignore
    """A class for a topic creation form."""

    title = TextAreaField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create topic")


class PostForm(FlaskForm):  # type: ignore
    """A class for a post creation form."""

    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Create post")
