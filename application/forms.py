from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Фамилия пользователя', validators=[DataRequired(), Length(min=2, max=50)])
    patronymic = StringField('Отчество пользователя (если имеется)', validators=[Length(min=2, max=50)])
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите ввод пароля', validators=[DataRequired(), EqualTo('password')])
    checkbox = BooleanField('Я даю согласие на обработку персональных данных', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Авторизоваться')
