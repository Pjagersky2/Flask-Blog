from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flaskblog.models import User


class RegistrationForm(FlaskForm):
    """
    Pass
    """

    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=2,
                                                          max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(),
                                                 EqualTo("password")])

    submit = SubmitField("Sign Up")

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("Error: Username is already taken.")

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError("Error: Email is already taken.")


class LoginForm(FlaskForm):
    """
    Pass
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    remember = BooleanField("Remember me")
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
