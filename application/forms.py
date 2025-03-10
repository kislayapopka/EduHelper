from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateTimeField
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, \
    MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from application.models.user import User


class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Фамилия пользователя', validators=[DataRequired(), Length(min=2, max=50)])
    patronymic = StringField('Отчество пользователя (если имеется)', validators=[Length(min=2, max=50)])
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите ввод пароля', validators=[DataRequired(), EqualTo('password')])
    checkbox = BooleanField('Я даю согласие на обработку персональных данных', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Данный адрес электронной почты уже есть в системе')


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизоваться')


class PostForm(FlaskForm):
    caption = StringField("Название задания", validators=[DataRequired()])
    body = TextAreaField("Описание задания", validators=[DataRequired()])
    due_date = DateTimeField("Срок выполнения", format="%Y-%m-%d %H:%M", validators=[DataRequired()])
    attached_files = MultipleFileField("Прикрепленные файлы", validators=[FileAllowed(
        ['pdf', 'docx', 'png', 'jpg', 'jpeg', 'zip'], "Недопустимый формат файла!")])
    student_groups = SelectMultipleField("Выберите группы студентов", coerce=int)
    submit = SubmitField("Создать задание")
