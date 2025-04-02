from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(),
        Length(min=4, max=25)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('password', message='Senhas devem ser iguais')
    ])
    submit = SubmitField('Registrar')

class ResetPasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[DataRequired()])
    new_password = PasswordField('Nova Senha', validators=[
        DataRequired(),
        Length(min=8, message='A senha deve ter pelo menos 8 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(),
        EqualTo('new_password', message='As senhas devem ser iguais')
    ])
    submit = SubmitField('Atualizar Senha')