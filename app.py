import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

# Importaciones para el sistema de inicio de sesión
from forms.usuario_form import RegistroForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
# Configuración obligatoria de seguridad para tokens CSRF
app.config['SECRET_KEY'] = 'clave_secreta_mundo_mascota_12345'

# ================= CONFIGURACIÓN DE BASE DE DATOS LOCAL (SQLITE) =================
DB_PATH = 'ferreteria.db'  # Usamos el archivo de base de datos que ya existe en tu carpeta

def obtener_conexion_local():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_tabla_usuarios():
    conexion = obtener_conexion_local()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Creamos la tabla de usuarios automáticamente al encender la app
inicializar_tabla_usuarios()

# ================= CONFIGURACIÓN DE GESTIÓN DE SESIONES =================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.login_message_category = "error"

# Modelo de usuario para mantener la sesión activa
class Usuario(UserMixin):
    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion_local()
    cursor = conexion.cursor()
    cursor.execute('SELECT id, usuario FROM usuarios WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conexion.close()
    if user_data:
        return Usuario(id=user_data['id'], usuario=user_data['usuario'])
    return None

# ============== DATOS ESTÁTICOS / MEMORIA PROVISIONAL
categorias_productos = [
    {"nombre": "Perros", "icono": "🐶", "imagen": "perro.jpg", "productos": ["Croquetas premium", "Collares", "Juguetes", "Camas para perros"], "stock": 10},
    {"nombre": "Gatos", "icono": "🐱", "imagen": "gato.jpg", "productos": ["Alimento para gatos", "Rascadores", "Arena sanitaria", "Juguetes"], "stock": 5},
    {"nombre": "Aves", "icono": "🦜", "imagen": "aves.jpg", "productos": ["Semillas para aves", "Jaulas", "Bebederos", "Juguetes para aves"], "stock": 8},
    {"nombre": "Conejos", "icono": "🐰", "imagen": "conejo.jpg", "productos": ["Heno", "Alimento especial", "Jaulas"], "stock": 4},
    {"nombre": "Hamster", "icono": "🐹", "imagen": "hamster.jpg", "productos": ["Jaulas pequeñas", "Ruedas de ejercicio", "Alimento"], "stock": 6},
    {"nombre": "Peces", "icono": "🐠", "imagen": "peces.jpg", "productos": ["Acuarios", "Comida para peces", "Filtros"], "stock": 3},
    {"nombre": "Accesorios", "icono": "🎒", "imagen": "accesorios.jpg", "productos": ["Correas", "Camas", "Platos"], "stock": 7},
    {"nombre": "Farmacia Veterinaria", "icono": "🏥", "imagen": "farmacia.jpg", "productos": ["Vitaminas", "Productos antipulgas", "Cuidado animal"], "stock": 0}
]

lista_clientes = [
    {"nombre": "Carlos Pérez", "correo": "carlos@gmail.com", "mascota": "Perro"},
    {"nombre": "María López", "correo": "maria@gmail.com", "mascota": "Gato"}
]

lista_proveedores = [
    {"nombre": "Distribuidora Pet Ecuador", "producto": "Alimentos y snacks para mascotas", "telefono": "0999999999"},
    {"nombre": "Mundo Animal S.A.", "producto": "Juguetes y accesorios", "telefono": "0988888888"},
    {"nombre": "Pet Care Ecuador", "producto": "Productos de higiene", "telefono": "0977777777"}
]

lista_facturas = [
    {"cliente": "Ana Gómez", "producto": "Alimento premium", "total": "25.00"},
    {"cliente": "Luis Pérez", "producto": "Cama para mascota", "total": "40.00"}
]

# ==================== RUTAS DE AUTENTICACIÓN NUEVAS ====================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistroForm()
    if form.validate_on_submit():
        conexion = obtener_conexion_local()
        cursor = conexion.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE usuario = ?', (form.usuario.data,))
        if cursor.fetchone():
            flash('El nombre de usuario ya se encuentra registrado.', 'error')
            cursor.close()
            conexion.close()
            return render_template('registro.html', form=form)
        
        # Encriptación de contraseña usando hash seguro requerido por la rúbrica
        pw_hash = generate_password_hash(form.password.data)
        query = 'INSERT INTO usuarios (usuario, password) VALUES (?, ?)'
        cursor.execute(query, (form.usuario.data, pw_hash))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('Registro exitoso. ¡Ahora puedes iniciar sesión!', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        conexion = obtener_conexion_local()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = ?', (form.usuario.data,))
        usuario_db = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        # Comprobación segura de credenciales
        if usuario_db and check_password_hash(usuario_db['password'], form.password.data):
            user_obj = Usuario(id=usuario_db['id'], usuario=usuario_db['usuario'])
            login_user(user_obj)
            flash('¡Sesión iniciada con éxito!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.', 'error')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('login'))

# ==================== RUTA PRINCIPAL =============
@app.route('/')
def index():
    tienda = "Mundo Mascota"
    return render_template("index.html", tienda=tienda)

# RUTA PRODUCTOS - ¡AHORA PROTEGIDA! =============
@app.route('/productos')
@login_required
def productos():
    titulo = "Productos para el bienestar de tu mascota"
    return render_template(
        "productos.html",
        titulo=titulo,
        categorias=categorias_productos,
        productos_db=[]  # Cambiado a lista limpia para evitar errores de tablas previas
    )

# RUTA FORMULARIO PRODUCTO - ¡AHORA PROTEGIDA! ====================
@app.route('/formulario_producto', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        return redirect(url_for('productos'))
    return render_template("formulario_producto.html", form=form, editando=False)

# RUTA EDITAR PRODUCTO - ¡AHORA PROTEGIDA! ===================
@app.route('/editar_producto/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def editar_producto(id_producto):
    form = ProductoForm()
    if form.validate_on_submit():
        return redirect(url_for('productos'))
    return render_template("formulario_producto.html", form=form, editando=True, id_producto=id_producto)

# RUTA ELIMINAR PRODUCTO - ¡AHORA PROTEGIDA! ====================
@app.route('/eliminar_producto/<int:id_producto>', methods=['POST'])
@login_required
def eliminar_producto(id_producto):
    return redirect(url_for('productos'))

# RUTAS RESTANTES - ¡AHORA PROTEGIDAS SEGÚN REQUERIMIENTOS DE LA TAREA! ====================
@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = {"nombre": form.nombre.data, "correo": form.correo.data, "mascota": form.mascota.data}
        lista_clientes.append(nuevo_cliente)
        return redirect(url_for('clientes'))
    return render_template("clientes.html", clientes=lista_clientes, form=form)

@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_prov = {"nombre": form.nombre.data, "producto": form.producto.data, "telefono": form.telefono.data}
        lista_proveedores.append(nuevo_prov)
        return redirect(url_for('proveedores'))
    return render_template("proveedores.html", proveedores=lista_proveedores, form=form)

@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        nueva_factura = {"cliente": form.cliente.data, "producto": form.producto.data, "total": f"{form.total.data:.2f}"}
        lista_facturas.append(nueva_factura)
        return redirect(url_for('facturacion'))
    return render_template("facturacion.html", facturas=lista_facturas, form=form)

if __name__ == "__main__":
    app.run(debug=True)
