from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    cliente = StringField('Cliente', validators=[
        DataRequired(message="El nombre del cliente es obligatorio")
    ])
    producto = SelectField('Producto', choices=[
        ('', 'Seleccione producto'),
        ('Alimento premium', 'Alimento premium'),
        ('Juguetes para mascotas', 'Juguetes para mascotas'),
        ('Camas para mascotas', 'Camas para mascotas'),
        ('Accesorios', 'Accesorios')
    ], validators=[DataRequired(message="Seleccione un producto")])
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria"),
        NumberRange(min=1, message="La cantidad debe ser al menos 1")
    ])
    total = DecimalField('Total', validators=[
        DataRequired(message="El total es obligatorio"),
        NumberRange(min=0.01, message="El total debe ser mayor a 0")
    ])
    submit = SubmitField('Generar factura')
