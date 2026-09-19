from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistroForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[
        DataRequired(message="El nombre de usuario es obligatorio"),
        Length(min=4, max=50, message="El usuario debe tener entre 4 y 50 caracteres")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria"),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres")
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message="Por favor confirma tu contraseña"),
        EqualTo('password', message="Las contraseñas deben coincidir")
    ])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[
        DataRequired(message="El usuario es obligatorio")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria")
    ])
    submit = SubmitField('Iniciar Sesión')
