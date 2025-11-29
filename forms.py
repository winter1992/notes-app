from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class NoteForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=200)])
    content = TextAreaField("Содержимое", validators=[DataRequired()])
    submit = SubmitField("Сохранить")

class AuthForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Отправить")