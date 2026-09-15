import os
from flask import Flask, render_template, request, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

# Importamos la conexión hacia tu base de datos MySQL
from conexion.conexion import obtener_conexion

app = Flask(__name__)

# Configuración obligatoria de seguridad para tokens CSRF
app.config['SECRET_KEY'] = 'clave_secreta_mundo_mascota_12345'

# ============== DATOS ESTÁTICOS / MEMORIA PROVISIONAL
categorias_productos = [
    {"nombre": "Perros", "icono": "🐾", "imagen": "perro.jpg", "productos": ["Croquetas premium", "Collares", "Juguetes", "Camas para perros"], "stock": 10},
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

# ==================== RUTA PRINCIPAL =============
@app.route('/')
def index():
    tienda = "Mundo Mascota"
    return render_template("index.html", tienda=tienda)

# ==================== RUTA PRODUCTOS (LISTAR - SELECT) =============
@app.route('/productos')
def productos():
    titulo = "Productos para el bienestar de tu mascota"
    
    conexion = obtener_conexion()
    productos_guardados = []
    
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT id_producto, nombre, descripcion, categoria FROM productos')
        productos_guardados = cursor.fetchall()  # Recupera los registros reales de MySQL
        cursor.close()
        conexion.close()
        
    return render_template(
        "productos.html",
        titulo=titulo,
        categorias=categorias_productos,
        productos_db=productos_guardados
    )

# ==================== RUTA FORMULARIO PRODUCTO (AGREGAR - INSERT) ====================
@app.route('/formulario_producto', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    
    if form.validate_on_submit():
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            query = 'INSERT INTO productos (nombre, descripcion, categoria) VALUES (%s, %s, %s)'
            valores = (form.nombre.data, form.descripcion.data, form.categoria.data)
            
            cursor.execute(query, valores)
            conexion.commit()  # Guardar los cambios reales
            cursor.close()
            conexion.close()
        return redirect(url_for('productos'))
        
    return render_template("formulario_producto.html", form=form, editando=False)

# ==================== RUTA EDITAR PRODUCTO (MODIFICAR - UPDATE) ====================
@app.route('/editar_producto/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    conexion = obtener_conexion()
    if not conexion:
        return redirect(url_for('productos'))
        
    cursor = conexion.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    producto = cursor.fetchone()
    
    if not producto:
        cursor.close()
        conexion.close()
        return redirect(url_for('productos'))
        
    form = ProductoForm()
    
    if request.method == 'GET':
        form.nombre.data = producto['nombre']
        form.descripcion.data = producto['descripcion']
        form.categoria.data = producto['categoria']
        
    if form.validate_on_submit():
        query = 'UPDATE productos SET nombre = %s, descripcion = %s, categoria = %s WHERE id_producto = %s'
        valores = (form.nombre.data, form.descripcion.data, form.categoria.data, id_producto)
        
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('productos'))
        
    cursor.close()
    conexion.close()
    return render_template("formulario_producto.html", form=form, editando=True, id_producto=id_producto)

# ==================== RUTA ELIMINAR PRODUCTO (ELIMINAR - DELETE) ====================
@app.route('/eliminar_producto/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect(url_for('productos'))

# =================== RUTAS RESTANTES (IGUALES A ANTES) ====================
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = {"nombre": form.nombre.data, "correo": form.correo.data, "mascota": form.mascota.data}
        lista_clientes.append(nuevo_cliente)
        return redirect(url_for('clientes'))
    return render_template("clientes.html", clientes=lista_clientes, form=form)

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_prov = {"nombre": form.nombre.data, "producto": form.producto.data, "telefono": form.telefono.data}
        lista_proveedores.append(nuevo_prov)
        return redirect(url_for('proveedores'))
    return render_template("proveedores.html", proveedores=lista_proveedores, form=form)

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        nueva_factura = {"cliente": form.cliente.data, "producto": form.producto.data, "total": f"{form.total.data:.2f}"}
        lista_facturas.append(nueva_factura)
        return redirect(url_for('facturacion'))
    return render_template("facturacion.html", facturas=lista_facturas, form=form)

if __name__ == "__main__":
    app.run(debug=True)
