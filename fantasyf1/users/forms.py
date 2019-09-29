from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from fantasyf1.models import User, Team
from fantasyf1.users.utils import get_driver_list, get_constructor_list

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update profile picture", validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField("Update")



    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists.")

class RequestResetForm(FlaskForm):
     email = StringField("Email", validators=[DataRequired(), Email()])
     submit = SubmitField("Get a new password")

     def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email not found")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset password")

class CreateTeamForm(FlaskForm):
    team_name = StringField("name", validators=[DataRequired(), Length(min=2, max=20)])
    primary_driver = SelectField("Primary driver", validators=[DataRequired()], choices=get_driver_list())
    secondary_driver = SelectField("Secondary driver", validators=[DataRequired()], choices=get_driver_list())
    team = SelectField("Team", validators=[DataRequired()], choices=get_constructor_list())
    submit = SubmitField("Post")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        
        if self.primary_driver.data == self.secondary_driver.data:
            self.secondary_driver.errors.append('Please, select two different drivers')
            return False
        
        return True