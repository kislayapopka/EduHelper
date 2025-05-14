from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateTimeField
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, \
    MultipleFileField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email

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


class UserForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Фамилия пользователя', validators=[DataRequired(), Length(min=2, max=50)])
    patronymic = StringField('Отчество пользователя (если имеется)', validators=[Length(min=2, max=50)])
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Length(min=2, max=50)])
    role = StringField('Роль пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Данный адрес электронной почты уже есть в системе')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Email(message="Неверный формат email")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Поле обязательно для заполнения")
    ])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    course_id = HiddenField("Course ID")
    caption = StringField("Название задания", validators=[DataRequired()])
    body = TextAreaField("Описание задания", validators=[DataRequired()])
    due_date = DateTimeField("Срок выполнения", format="%d.%m.%Y %H:%M")
    attached_files = MultipleFileField("Прикрепленные файлы", validators=[FileAllowed(
        ['pdf', 'docx', 'png', 'jpg', 'jpeg', 'zip'], "Недопустимый формат файла!")])
    is_info = BooleanField('Информационный пост')
    submit = SubmitField("Создать публикацию")


class EditPostForm(FlaskForm):
    course_id = HiddenField("Course ID")
    caption = StringField('Заголовок', validators=[DataRequired()])
    body = TextAreaField('Текст', validators=[DataRequired()])
    due_date = DateTimeField("Срок выполнения", format="%d.%m.%Y %H:%M", validators=[DataRequired()])
    attached_files = MultipleFileField("Прикрепленные файлы", validators=[FileAllowed(
        ['pdf', 'docx', 'png', 'jpg', 'jpeg', 'zip'], "Недопустимый формат файла!")])
    submit = SubmitField("Изменить публикацию")


class SubmissionForm(FlaskForm):
    submission_id = HiddenField("Submission ID")
    post_id = HiddenField("Post ID")
    user_id = HiddenField("User ID")
    attached_files = MultipleFileField("Прикрепленные файлы", validators=[FileAllowed(
        ['pdf', 'docx', 'png', 'jpg', 'jpeg', 'zip'], "Недопустимый формат файла!")])
    submit = SubmitField("Добавить выполнение")


class JoinCourseForm(FlaskForm):
    code = StringField(
        "Код курса",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Введите уникальный код курса"}
    )
    submit = SubmitField(
        "Присоединиться к курсу",
        render_kw={"class": "btn btn-primary"}
    )


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
