import os
from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import obtener_conexion

# Formularios
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import RegistroForm, LoginForm

# Autenticación
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_mundo_mascota_12345'

# ================= GESTIÓN DE SESIONES =================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.login_message_category = "error"

class Usuario(UserMixin):
    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor()
    cursor.execute('SELECT id, usuario FROM usuarios WHERE id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conexion.close()
    if user_data:
        return Usuario(id=user_data['id'], usuario=user_data['usuario'])
    return None

# Categorías estáticas para mantener el diseño visual intacto
categorias_productos = [
    {"nombre": "Perros", "icono": "🐶", "imagen": "perro.jpg", "productos": ["Croquetas premium", "Collares"], "stock": 10},
    {"nombre": "Gatos", "icono": "🐱", "imagen": "gato.jpg", "productos": ["Alimento para gatos", "Rascadores"], "stock": 5},
    {"nombre": "Aves", "icono": "🦜", "imagen": "aves.jpg", "productos": ["Semillas para aves"], "stock": 8},
    {"nombre": "Conejos", "icono": "🐰", "imagen": "conejo.jpg", "productos": ["Heno"], "stock": 4},
    {"nombre": "Hamster", "icono": "🐹", "imagen": "hamster.jpg", "productos": ["Ruedas de ejercicio"], "stock": 6},
    {"nombre": "Peces", "icono": "🐠", "imagen": "peces.jpg", "productos": ["Acuarios"], "stock": 3},
    {"nombre": "Accesorios", "icono": "🎒", "imagen": "accesorios.jpg", "productos": ["Correas"], "stock": 7},
    {"nombre": "Farmacia Veterinaria", "icono": "🏥", "imagen": "farmacia.jpg", "productos": ["Vitaminas"], "stock": 0}
]

# ================= RUTAS DE AUTENTICACIÓN =================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistroForm()
    if form.validate_on_submit():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        if cursor.fetchone():
            flash('El nombre de usuario ya se encuentra registrado.', 'error')
            cursor.close()
            conexion.close()
            return render_template('registro.html', form=form)
        
        pw_hash = generate_password_hash(form.password.data)
        cursor.execute('INSERT INTO usuarios (usuario, password) VALUES (%s, %s)', (form.usuario.data, pw_hash))
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
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        usuario_db = cursor.fetchone()
        cursor.close()
        conexion.close()
        
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

# ================= RUTA PRINCIPAL =================
@app.route('/')
def index():
    return render_template("index.html", tienda="Mundo Mascota")

# ================= CONTROL CRUD PRODUCTOS (POSTGRESQL) =================

# LEER (SELECT con consulta JOIN)
@app.route('/productos')
@login_required
def productos():
    titulo = "Productos para el bienestar de tu mascota"
    conexion = obtener_conexion()
    productos_lista = []
    if conexion:
        cursor = conexion.cursor()
        # Consulta JOIN requerida para vincular productos con proveedores
        query = """
            SELECT p.id_producto, p.nombre, p.descripcion, p.categoria 
            FROM productos p 
            LEFT JOIN proveedores prov ON p.id_proveedor = prov.id_proveedor
            ORDER BY p.id_producto DESC
        """
        cursor.execute(query)
        productos_lista = cursor.fetchall()
        cursor.close()
        conexion.close()
        
    return render_template(
        "productos.html",
        titulo=titulo,
        categorias=categorias_productos,
        productos_db=productos_lista
    )

# CREAR (INSERT)
@app.route('/formulario_producto', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = "INSERT INTO productos (nombre, descripcion, categoria) VALUES (%s, %s, %s)"
            cursor.execute(query, (form.nombre.data, form.descripcion.data, form.categoria.data))
            conexion.commit()
            cursor.close()
            conexion.close()
            flash('Producto registrado con éxito en PostgreSQL', 'success')
            return redirect(url_for('productos'))
    return render_template("formulario_producto.html", form=form, editando=False)

# ACTUALIZAR (UPDATE)
@app.route('/editar_producto/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def editar_producto(id_producto):
    form = ProductoForm()
    conexion = obtener_conexion()
    
    if request.method == 'GET':
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
            prod = cursor.fetchone()
            cursor.close()
            conexion.close()
            if prod:
                form.nombre.data = prod['nombre']
                form.descripcion.data = prod['descripcion']
                form.categoria.data = prod['categoria']

    if form.validate_on_submit():
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE productos SET nombre = %s, descripcion = %s, categoria = %s WHERE id_producto = %s"
            cursor.execute(query, (form.nombre.data, form.descripcion.data, form.categoria.data, id_producto))
            conexion.commit()
            cursor.close()
            conexion.close()
            flash('Producto actualizado correctamente', 'success')
            return redirect(url_for('productos'))
            
    return render_template("formulario_producto.html", form=form, editando=True, id_producto=id_producto)

# ELIMINAR (DELETE)
@app.route('/eliminar_producto/<int:id_producto>', methods=['POST'])
@login_required
def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        query = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(query, (id_producto,))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('Producto eliminado permanentemente', 'success')
    return redirect(url_for('productos'))

# ================= SECCIONES ADICIONALES (MEMORIA PROVISIONAL) =================
@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    # Lista temporal simulada para no alterar la visualización de clientes
    lista_clientes = [
        {"nombre": "Carlos Pérez", "correo": "carlos@gmail.com", "mascota": "Perro"},
        {"nombre": "María López", "correo": "maria@gmail.com", "mascota": "Gato"}
    ]
    if form.validate_on_submit():
        nuevo = {"nombre": form.nombre.data, "correo": form.correo.data, "mascota": form.mascota.data}
        lista_clientes.append(nuevo)
        return redirect(url_for('clientes'))
    return render_template("clientes.html", clientes=lista_clientes, form=form)

@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():
    form = ProveedorForm()
    lista_proveedores = [
        {"nombre": "Distribuidora Pet Ecuador", "producto": "Alimentos", "telefono": "0999999999"}
    ]
    if form.validate_on_submit():
        nuevo = {"nombre": form.nombre.data, "producto": form.producto.data, "telefono": form.telefono.data}
        lista_proveedores.append(nuevo)
        return redirect(url_for('proveedores'))
    return render_template("proveedores.html", proveedores=lista_proveedores, form=form)

@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():
    form = FacturacionForm()
    lista_facturas = [
