from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateTimeField
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, \
    MultipleFileField, HiddenField
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
    course_id = HiddenField("Course ID")
    caption = StringField("Название задания", validators=[DataRequired()])
    body = TextAreaField("Описание задания", validators=[DataRequired()])
    due_date = DateTimeField("Срок выполнения", format="%Y-%m-%d %H:%M", validators=[DataRequired()])
    attached_files = MultipleFileField("Прикрепленные файлы", validators=[FileAllowed(
        ['pdf', 'docx', 'png', 'jpg', 'jpeg', 'zip'], "Недопустимый формат файла!")])
    submit = SubmitField("Создать задание")


class JoinCourseForm(FlaskForm):
    code = StringField("Введите уникальный код курса", validators=[DataRequired()])
    submit = SubmitField("Присоединиться к курсу")


class CreateCourseForm(FlaskForm):
    name = StringField(
        "Название курса",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Введите название курса"}
    )
    description = TextAreaField(
        "Описание курса (опционально)",
        render_kw={"class": "form-control", "rows": 3}
    )
    submit = SubmitField(
        "Создать курс",
        render_kw={"class": "btn btn-primary"}
    )
