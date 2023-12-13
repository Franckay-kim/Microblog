from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, length
import sqlalchemy as sa
from flask_babel import lazy_gettext as _1
from app import db
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_1('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_1('About me'), validators=[length(min=0, max=140)])
    submit = SubmitField(_1('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            # user = User.query.filter_by(username=self.username.data).first()
            user = db.session.scalar(sa.select(User).where(User.username == self.username.data))
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


# empty form for following and unfollowing
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


# Blog submission form
class PostForm(FlaskForm):
    post = TextAreaField(_1('Say Something'), validators=[DataRequired()])
    submit = SubmitField(_1('Submit'))

