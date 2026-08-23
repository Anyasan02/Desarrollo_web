from flask import Flask, render_template

app = Flask(__name__)

# ==================== DATOS DINÁMICOS DE PRODUCTOS ====================
categorias_productos = [
    {
        "nombre": "Perros",
        "icono": "🐶",
        "imagen": "perro.jpg",
        "productos": [
            "Croquetas premium",
            "Collares",
            "Juguetes",
            "Camas para perros"
        ],
        "stock": 10
    },
    {
        "nombre": "Gatos",
        "icono": "🐱",
        "imagen": "gato.jpg",
        "productos": [
            "Alimento para gatos",
            "Rascadores",
            "Arena sanitaria",
            "Juguetes"
        ],
        "stock": 5
    },
    {
        "nombre": "Aves",
        "icono": "🦜",
        "imagen": "aves.jpg",
        "productos": [
            "Semillas para aves",
            "Jaulas",
            "Bebederos",
            "Juguetes para aves"
        ],
        "stock": 8
    },
    {
        "nombre": "Conejos",
        "icono": "🐰",
        "imagen": "conejo.jpg",
        "productos": [
            "Heno",
            "Alimento especial",
            "Jaulas"
        ],
        "stock": 4
    },
    {
        "nombre": "Hamster",
        "icono": "🐹",
        "imagen": "hamster.jpg",
        "productos": [
            "Jaulas pequeñas",
            "Ruedas de ejercicio",
            "Alimento"
        ],
        "stock": 6
    },
    {
        "nombre": "Peces",
        "icono": "🐟",
        "imagen": "peces.jpg",
        "productos": [
            "Acuarios",
            "Comida para peces",
            "Filtros"
        ],
        "stock": 3
    },
    {
        "nombre": "Accesorios",
        "icono": "🎒",
        "imagen": "accesorios.jpg",
        "productos": [
            "Correas",
            "Camas",
            "Platos"
        ],
        "stock": 7
    },
    {
        "nombre": "Farmacia Veterinaria",
        "icono": "💊",
        "imagen": "farmacia.jpg",
        "productos": [
            "Vitaminas",
            "Productos antipulgas",
            "Cuidado animal"
        ],
        "stock": 0
    }
]

# ==================== RUTA PRINCIPAL ====================
@app.route('/')
def index():
    tienda = "Mundo Mascota"
    return render_template(
        "index.html",
        tienda=tienda
    )

# ==================== RUTA PRODUCTOS ====================
@app.route('/productos')
def productos():
    titulo = "Productos para el bienestar de tu mascota"
    return render_template(
        "productos.html",
        titulo=titulo,
        categorias=categorias_productos
    )

# ==================== RUTA CLIENTES ====================
@app.route('/clientes')
def clientes():
    lista_clientes = [
        {
            "nombre": "Carlos Pérez",
            "correo": "carlos@gmail.com",
            "mascota": "Perro"
        },
        {
            "nombre": "María López",
            "correo": "maria@gmail.com",
            "mascota": "Gato"
        }
    ]
    return render_template(
        "clientes.html",
        clientes=lista_clientes
    )

# ==================== RUTA PROVEEDORES ====================
@app.route('/proveedores')
def proveedores():
    return render_template(
        "proveedores.html"
    )

# ==================== RUTA FACTURACIÓN ====================
@app.route('/facturacion')
def facturacion():
    return render_template(
        "facturacion.html"
    )

if __name__ == "__main__":
    app.run(debug=True)
