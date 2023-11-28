from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, length
from flask_babel import _, lazy_gettext as _1
from .models import User


class LoginForm(FlaskForm):
    username = StringField(_1('Username'), validators=[DataRequired()])
    password = PasswordField(_1('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_1('Remember Me'))
    submit = SubmitField(_1('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_1('Username'), validators=[DataRequired()])
    email = StringField(_1('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_1('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _1('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_1('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_1('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_1('Please use a different email address.'))


class EditProfileForm(FlaskForm):
    username = StringField(_1('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_1('About me'), validators=[length(min=0, max=140)])
    submit = SubmitField(_1('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_1('Please use a different username.'))


# empty form for following and unfollowing
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


# Blog submission form
class PostForm(FlaskForm):
    post = TextAreaField(_1('Say Something'), validators=[
        DataRequired(), length(min=1, max=140)])
    submit = SubmitField(_1('Submit'))


# Reset password request form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_1('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_1('Request Password Reset'))


# password reset form
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_1('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _1('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_1('Request Password Reset'))
