import psycopg2

try:
    servidor = "dpg-dassc617lnhs73ak44bg-a" + ".ohio-postgres" + ".render.com"
    usuario_db = "mundo_mascota_db_user"
    clave_db = "NwMjdKgygjMZNLwFUhyqdwEJSiywa1Vr"
    nombre_db = "mundo_mascota_db"
    
    url = f"postgresql://{usuario_db}:{clave_db}@{servidor}/{nombre_db}"
    
    print("Conectando a Render...")
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    
    print("Creando estructura completa de tablas...")
    
    # 1. Tabla Usuarios
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, usuario VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL);")
    
    # 2. Tabla Proveedores 
    cursor.execute("CREATE TABLE IF NOT EXISTS proveedores (id_proveedor SERIAL PRIMARY KEY, nombre VARCHAR(100) NOT NULL, producto VARCHAR(100), telefono VARCHAR(20));")
    
    # 3. Tabla Clientes 
    cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id_cliente SERIAL PRIMARY KEY, nombre VARCHAR(100) NOT NULL, correo VARCHAR(100), telefono VARCHAR(20), mascota VARCHAR(50));")
    
    # 4. Tabla Productos
    cursor.execute("CREATE TABLE IF NOT EXISTS productos (id_producto SERIAL PRIMARY KEY, nombre VARCHAR(100) NOT NULL, descripcion TEXT, categoria VARCHAR(50), id_proveedor INT REFERENCES proveedores(id_proveedor) ON DELETE SET NULL);")
    
    # 5. Tabla Facturas 
    cursor.execute("CREATE TABLE IF NOT EXISTS facturas (id_factura SERIAL PRIMARY KEY, cliente VARCHAR(100) NOT NULL, producto VARCHAR(100) NOT NULL, cantidad INT, total NUMERIC(10,2));")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("¡Todas las tablas creadas y corregidas con éxito!")

except Exception as e:
    print(f"Error: {e}")
