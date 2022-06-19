from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    movie1 = StringField('영화1', validators=[DataRequired(), Length(min=2, max=100)])
    movie2 = StringField('영화2', validators=[DataRequired(), Length(min=2, max=100)])
    movie3 = StringField('영화3', validators=[DataRequired(), Length(min=2, max=100)])
    movie4 = StringField('영화4', validators=[DataRequired(), Length(min=2, max=100)])
    movie5 = StringField('영화5', validators=[DataRequired(), Length(min=2, max=100)])
    rating1 = IntegerField('평점1', validators=[DataRequired(), NumberRange(min=1, max=5)])
    rating2 = IntegerField('평점2', validators=[DataRequired(), NumberRange(min=1, max=5)])
    rating3 = IntegerField('평점3', validators=[DataRequired(), NumberRange(min=1, max=5)])
    rating4 = IntegerField('평점4', validators=[DataRequired(), NumberRange(min=1, max=5)])
    rating5 = IntegerField('평점5', validators=[DataRequired(), NumberRange(min=1, max=5)])

class UserHistoryForm(FlaskForm):
    movie = StringField('영화', validators=[DataRequired(), Length(min=2, max=100)])
    rating = IntegerField('평점', validators=[DataRequired(), NumberRange(min=1, max=5)])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])