import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

# Configuración obligatoria de seguridad para tokens CSRF
app.config['SECRET_KEY'] = 'clave_secreta_mundo_mascota_12345'

# Ruta del archivo de la base de datos SQLite
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ferreteria.db')

# Asegurar que la carpeta 'data' exista antes de iniciar
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

def init_db():
    """Inicializa la base de datos y crea la tabla productos si no existe."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ejecutar la inicialización de la base de datos
init_db()


# ==================== DATOS ESTÁTICOS / MEMORIA PROVISIONAL ====================
# Se mantienen igual para la visualización de categorías en productos.html
categorias_productos = [
    {"nombre": "Perros", "icono": "🐶", "imagen": "perro.jpg", "productos": ["Croquetas premium", "Collares", "Juguetes", "Camas para perros"], "stock": 10},
    {"nombre": "Gatos", "icono": "🐱", "imagen": "gato.jpg", "productos": ["Alimento para gatos", "Rascadores", "Arena sanitaria", "Juguetes"], "stock": 5},
    {"nombre": "Aves", "icono": "🦜", "imagen": "aves.jpg", "productos": ["Semillas para aves", "Jaulas", "Bebederos", "Juguetes para aves"], "stock": 8},
    {"nombre": "Conejos", "icono": "🐰", "imagen": "conejo.jpg", "productos": ["Heno", "Alimento especial", "Jaulas"], "stock": 4},
    {"nombre": "Hamster", "icono": "🐹", "imagen": "hamster.jpg", "productos": ["Jaulas pequeñas", "Ruedas de ejercicio", "Alimento"], "stock": 6},
    {"nombre": "Peces", "icono": "🐠", "imagen": "peces.jpg", "productos": ["Acuarios", "Comida para peces", "Filtros"], "stock": 3},
    {"nombre": "Accesorios", "icono": "🦮", "imagen": "accesorios.jpg", "productos": ["Correas", "Camas", "Platos"], "stock": 7},
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


# ==================== RUTA PRINCIPAL ====================
@app.route('/')
def index():
    tienda = "Mundo Mascota"
    return render_template("index.html", tienda=tienda)


# ==================== RUTA PRODUCTOS ====================
@app.route('/productos')
def productos():
    titulo = "Productos para el bienestar de tu mascota"
    
    # CONSULTAR REGISTROS DE SQLITE (SELECT)
    conn = sqlite3.connect(DATABASE_PATH)
    # Cambiar el row_factory para interactuar con los resultados como diccionarios
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, descripcion, categoria FROM productos')
    productos_guardados = cursor.fetchall()
    conn.close()
    
    return render_template(
        "productos.html", 
        titulo=titulo, 
        categorias=categorias_productos, 
        productos_db=productos_guardados  # Enviamos la lista de la base de datos a la plantilla
    )


# ==================== RUTA FORMULARIO PRODUCTO ====================
@app.route('/formulario_producto', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    
    # VALIDACIÓN DEL LADO DEL SERVIDOR
    if form.validate_on_submit():
        # GUARDAR EN SQLITE (INSERT)
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Uso estricto de parámetros "?" para evitar inyecciones SQL
        cursor.execute(
            'INSERT INTO productos (nombre, descripcion, categoria) VALUES (?, ?, ?)',
            (form.nombre.data, form.descripcion.data, form.categoria.data)
        )
        
        conn.commit()  # Guardar los cambios
        conn.close()   # Cerrar la conexión de forma segura
        
        return redirect(url_for('productos'))
        
    return render_template("formulario_producto.html", form=form)


# ==================== RUTA CLIENTES ====================
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "mascota": form.mascota.data
        }
        lista_clientes.append(nuevo_cliente)
        return redirect(url_for('clientes'))
    return render_template("clientes.html", clientes=lista_clientes, form=form)


# ==================== RUTA PROVEEDORES ====================
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_prov = {
            "nombre": form.nombre.data,
            "producto": form.producto.data,
            "telefono": form.telefono.data
        }
        lista_proveedores.append(nuevo_prov)
        return redirect(url_for('proveedores'))
    return render_template("proveedores.html", proveedores=lista_proveedores, form=form)


# ==================== RUTA FACTURACIÓN ====================
@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        nueva_factura = {
            "cliente": form.cliente.data,
            "producto": form.producto.data,
            "total": f"{form.total.data:.2f}"
        }
        lista_facturas.append(nueva_factura)
        return redirect(url_for('facturacion'))
    return render_template("facturacion.html", facturas=lista_facturas, form=form)


if __name__ == "__main__":
    app.run(debug=True)
