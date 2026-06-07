-- =====================================================
-- CREACIÓN DE BASE DE DATOS
-- =====================================================

CREATE DATABASE IF NOT EXISTS gastronomia_db;
USE gastronomia_db;


-- =====================================================
-- TABLA: Usuarios
-- =====================================================

CREATE TABLE IF NOT EXISTS Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('cliente', 'admin'))
);


-- =====================================================
-- TABLA: Categorias
-- =====================================================

CREATE TABLE IF NOT EXISTS Categorias (
    categorias_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);


-- =====================================================
-- TABLA: Productos
-- =====================================================

CREATE TABLE IF NOT EXISTS Productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    categorias_id INT NOT NULL,
    descripcion VARCHAR(300),
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    FOREIGN KEY (categorias_id) REFERENCES Categorias(categorias_id) ON DELETE RESTRICT
);


-- =====================================================
-- TABLA: Servicios
-- =====================================================

CREATE TABLE IF NOT EXISTS Servicios (
    servicio_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);


-- =====================================================
-- TABLA: Reservas
-- =====================================================

CREATE TABLE IF NOT EXISTS Reservas (
    reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(12) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0),
    estado VARCHAR(30) NOT NULL DEFAULT 'reservada' CHECK (estado IN ('reservada', 'cancelada', 'finalizada')),
);


-- =====================================================
-- TABLA: Resenas
-- =====================================================

CREATE TABLE IF NOT EXISTS Resenas (
    resena_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL UNIQUE,
    puntuacion_ambiente INT NOT NULL CHECK (puntuacion_ambiente BETWEEN 1 AND 5),
    puntuacion_servicio INT NOT NULL CHECK (puntuacion_servicio BETWEEN 1 AND 5),
    puntuacion_comida INT NOT NULL CHECK (puntuacion_comida BETWEEN 1 AND 5),
    comentario TEXT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE
);


-- =====================================================
-- TABLA: Servicios_reserva
-- =====================================================

CREATE TABLE IF NOT EXISTS Servicios_reserva (
    servicios_reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL,
    servicio_id INT NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id) ON DELETE RESTRICT
);


-- =====================================================
-- TABLA: Mesas
-- =====================================================

CREATE TABLE IF NOT EXISTS Mesas (
    mesa_id INT PRIMARY KEY AUTO_INCREMENT,
    estado VARCHAR(20) NOT NULL DEFAULT 'desocupada' CHECK (estado IN ('ocupada', 'desocupada')),
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0)
);


-- =====================================================
-- DATOS INICIALES (INSERTS)
-- =====================================================

-- Usuario administrador 
INSERT IGNORE INTO Usuarios (usuario_id, nombre, apellido, nombre_usuario, email, contrasena, rol) 
VALUES (1, 'Kevin', 'La Rocca', 'kevin_dev', 'kevin@test.com', 'hashed_password_123', 'admin');

-- Categoría 
INSERT IGNORE INTO Categorias (categorias_id, nombre) 
VALUES (1, 'Platos Principales');

-- Producto 
INSERT IGNORE INTO Productos (producto_id, categorias_id, descripcion, nombre, precio) 
VALUES (1, 1, 'Milanesa con papas fritas', 'Milanesa Clásica', 1250.00);

-- Servicio 
INSERT IGNORE INTO Servicios (servicio_id, nombre) 
VALUES (1, 'Servicio de Prueba');

-- Reserva 
INSERT IGNORE INTO Reservas (reserva_id, fecha, email, nombre, apellido, DNI, telefono, cantidad_personas, estado) 
VALUES (1, '2026-06-15', 'test@gmail.com', 'Kevin', 'La Rocca', '44123456', '1123456789', 4, 'reservada');

-- Reseña 
INSERT IGNORE INTO Resenas (resena_id, reserva_id, puntuacion_ambiente, puntuacion_servicio, puntuacion_comida, comentario) 
VALUES (1, 1, 5, 5, 5, 'Excelente servicio y comida tremenda.');

-- Relación servicio-reserva 
INSERT IGNORE INTO Servicios_reserva (servicios_reserva_id, reserva_id, servicio_id) 
VALUES (1, 1, 1);

-- Mesa 
INSERT IGNORE INTO Mesas (mesa_id, estado, cantidad_personas) 
VALUES (1, 'desocupada', 4);