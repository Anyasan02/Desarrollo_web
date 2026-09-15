-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS mundo_mascota;
USE mundo_mascota;

-- Tabla de Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    producto VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

-- Tabla de Productos (Módulo seleccionado para control CRUD completo)
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) DEFAULT 0.00,
    stock INT DEFAULT 0,
    id_proveedor INT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    mascota VARCHAR(50) NOT NULL
);

-- Tabla de Facturas
CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NULL,
    cliente_nombre VARCHAR(100) NOT NULL,
    producto VARCHAR(100) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE SET NULL
);
