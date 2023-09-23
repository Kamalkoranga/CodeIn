from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField, StringField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    """The `LoginForm` class represents a form with fields for email and
    password inputs, as well as a submit button.

    Args:
        FlaskForm (_type_): inherits from the FlaskForm class
    """
    # Field for email input
    email = EmailField(
        'Email', validators=[DataRequired(), Email(), Length(1, 64)]
    )
    # Field for password input
    password = PasswordField('Password', validators=[DataRequired()])
    # Submit button field
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    """Define signup form fields
    The `RegistrationForm` class represents a form for user registration with
    fields for email, password, and a submit button.

    Args:
        FlaskForm (_type_): inherits from the FlaskForm class

    Raises:
        ValidationError: The email address is already registered
    """
    email = StringField(
        'Email',
        validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Join')

    # Custom validation method for the 'email' field
    def validate_email(self, field):
        """
        The function is used to validate an email address.

        :param field: The "field" parameter in the "validate_email" function
        is the email address that needs to be validated
        """
        # Check if the email already exists in the User table
        if User.query.filter_by(email=field.data.lower()).first():
            # Raise a validation error if the email is already registered
            raise ValidationError('Email already registered.')
