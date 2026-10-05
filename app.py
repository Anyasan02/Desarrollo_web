import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_123'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# URL Externa de la Base de Datos de Render
servidor_db = "dpg-dassc617lnhs73ak44bg-a" + ".ohio-postgres" + ".render.com"
DATABASE_URL = f"postgresql://mundo_mascota_db_user:NwMjdKgygjMZNLwFUhyqdwEJSiywa1Vr@{servidor_db}/mundo_mascota_db"

def obtener_conexion():
    return psycopg2.connect(DATABASE_URL)

class Usuario(UserMixin):
    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario

@login_manager.user_loader
def load_user(user_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return Usuario(user[0], user[1])
    return None

# --- FORMULARIOS ---
class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired()])
    correo = StringField('Correo electrónico', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    mascota = SelectField('Mascota', choices=[('Perro', 'Perro'), ('Gato', 'Gato'), ('Ave', 'Ave'), ('Conejo', 'Conejo')], validators=[DataRequired()])
    submit = SubmitField('Guardar cliente')

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre del proveedor', validators=[DataRequired()])
    producto = StringField('Producto suministrado', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Guardar proveedor')

class FacturacionForm(FlaskForm):
    cliente = StringField('Cliente', validators=[DataRequired()])
    producto = StringField('Producto', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    total = DecimalField('Total', validators=[DataRequired()])
    submit = SubmitField('Generar factura')

# --- RUTAS DE LA APLICACIÓN ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (usuario, password))
            conn.commit()
            return redirect(url_for('login'))
        except:
            return "El usuario ya existe."
        finally:
            cursor.close()
            conn.close()
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario FROM usuarios WHERE usuario = %s AND password = %s", (usuario, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            user_obj = Usuario(user[0], user[1])
            login_user(user_obj)
            return redirect(url_for('productos'))
    return render_template('login.html')

@app.route('/productos', methods=['GET', 'POST'])
@login_required
def productos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Hacemos la consulta JOIN requerida  para enlazar productos y proveedores
    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.categoria, prov.nombre 
        FROM productos p
        LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor
    """)
    productos_registrados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    lista_productos = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "categoria": p[3], "proveedor": p[4]} 
        for p in productos_registrados
    ]
    return render_template('productos.html', productos=lista_productos)


@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    if form.validate_on_submit():
        cursor.execute("INSERT INTO clientes (nombre, correo, telefono, mascota) VALUES (%s, %s, %s, %s)",
                       (form.nombre.data, form.correo.data, form.telefono.data, form.mascota.data))
        conn.commit()
        return redirect(url_for('clientes'))
        
    cursor.execute("SELECT nombre, correo, mascota FROM clientes")
    clientes_registrados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Formateamos los datos para la tabla HTML
    lista_clientes = [{"nombre": c[0], "correo": c[1], "mascota": c[2]} for c in clientes_registrados]
    return render_template('clientes.html', form=form, clientes=lista_clientes)

@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():
    form = ProveedorForm()
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    if form.validate_on_submit():
        cursor.execute("INSERT INTO proveedores (nombre, producto, telefono) VALUES (%s, %s, %s)",
                       (form.nombre.data, form.producto.data, form.telefono.data))
        conn.commit()
        return redirect(url_for('proveedores'))
        
    cursor.execute("SELECT nombre, producto, telefono FROM proveedores")
    proveedores_registrados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    lista_proveedores = [{"nombre": p[0], "producto": p[1], "telefono": p[2]} for p in proveedores_registrados]
    return render_template('proveedores.html', form=form, proveedores=lista_proveedores)

@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():
    form = FacturacionForm()
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    if form.validate_on_submit():
        cursor.execute("INSERT INTO facturas (cliente, producto, cantidad, total) VALUES (%s, %s, %s, %s)",
                       (form.cliente.data, form.producto.data, form.cantidad.data, form.total.data))
        conn.commit()
        return redirect(url_for('facturacion'))
        
    cursor.execute("SELECT cliente, producto, total FROM facturas")
    facturas_registradas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    lista_facturas = [{"cliente": f[0], "producto": f[1], "total": str(f[2])} for f in facturas_registradas]
    return render_template('facturacion.html', form=form, facturas=lista_facturas)

@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
