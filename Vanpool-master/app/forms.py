from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    """User Log-in Form."""
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                           ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired()
                             ])
    submit = SubmitField('Sign in')


class AddDriverForm(FlaskForm):
    submit = SubmitField('Add Driver')


class AssignDriverForm(FlaskForm):
    submit = SubmitField('Assign Driver')


class RegisterVehicleForm(FlaskForm):
    model = StringField('Model', validators=[DataRequired()])
    make = StringField('Make', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    license_plate = StringField('License Plate Number', validators=[DataRequired()])
    submit = SubmitField('Submit Vehicle Information')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class DestinationForm(FlaskForm):
    destination = StringField('Destination:', validators=[DataRequired()])
    submit = SubmitField('Submit your destination')


