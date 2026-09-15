from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=3, message="El nombre debe tener mínimo 3 caracteres")
    ])
    descripcion = TextAreaField('Descripción', validators=[
        DataRequired(message="La descripción es obligatoria"),
        Length(min=5, message="La descripción es demasiado corta")
    ])
    categoria = SelectField('Categoría', choices=[
        ('', 'Seleccione una categoría'),
        ('Perros', 'Perros'),
        ('Gatos', 'Gatos'),
        ('Aves', 'Aves'),
        ('Conejos', 'Conejos'),
        ('Hamster', 'Hamster'),
        ('Peces', 'Peces'),
        ('Accesorios', 'Accesorios'),
        ('Farmacia', 'Farmacia Veterinaria')
    ], validators=[DataRequired(message="Seleccione una categoría")])
    submit = SubmitField('Registrar Producto')
