from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from market.models import User


class RegistrationForm(FlaskForm):

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Invalid username. Username already exists")

    def validate_email_address(self, field):
        user = User.query.filter_by(email_address=field.data).first()
        if user:
            raise ValidationError("Email address already taken")

    username = StringField(
        label="Username",
        validators=[DataRequired(),
                    Length(min=2,
                           max=30,
                           message="Username should have a minimum of 6 character and maximum of 30 characters")
                    ],
        id="username"
    )

    email_address = EmailField(label="Email", validators=[DataRequired()], id="email_address")

    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Password should match"), Length(min=6)
        ]
    )
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], id="username")
    password = PasswordField("Password", validators=[DataRequired()], id="password")
    submit = SubmitField("Sign In")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError("Invalid username and password.")


class PurchaseForm(FlaskForm):
    submit = SubmitField("Purchase Item")


class SellItemForm(FlaskForm):
    submit = SubmitField("Sell Item")

