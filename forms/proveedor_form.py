from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre del proveedor', validators=[
        DataRequired(message="El nombre del proveedor es obligatorio")
    ])
    producto = StringField('Producto suministrado', validators=[
        DataRequired(message="El producto suministrado es obligatorio")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono de contacto es obligatorio")
    ])
    submit = SubmitField('Guardar proveedor')
