from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal (Llama a tu index.html de mascotas)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el módulo de Productos
@app.route('/productos')
def productos():
    return render_template('productos.html')

# Ruta para el módulo de Clientes
@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

# Ruta para el módulo de Proveedores
@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

# Ruta para el módulo de Facturación
@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')

if __name__ == '__main__':
    app.run(debug=True)
