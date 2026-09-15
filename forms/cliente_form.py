from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[
        DataRequired(message="El nombre completo es obligatorio")
    ])
    correo = StringField('Correo electrónico', validators=[
        DataRequired(message="El correo electrónico es obligatorio"),
        Email(message="Ingrese un correo electrónico válido")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El número de teléfono es obligatorio")
    ])
    mascota = SelectField('Mascota', choices=[
        ('', 'Seleccione mascota'),
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Conejo', 'Conejo'),
        ('Hamster', 'Hamster')
    ], validators=[DataRequired(message="Seleccione una mascota")])
    submit = SubmitField('Guardar cliente')
