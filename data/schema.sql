SET NAMES 'utf8mb4';

-- CREACIÓN DE BASE DE DATOS
CREATE DATABASE IF NOT EXISTS gastronomia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gastronomia_db;

--  codificacion
ALTER DATABASE `gastronomia_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- TABLA: Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('cliente', 'admin'))
);

-- TABLA: Categorias
CREATE TABLE IF NOT EXISTS Categorias (
    categorias_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- TABLA: Productos
CREATE TABLE IF NOT EXISTS Productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    categorias_id INT NOT NULL,
    descripcion VARCHAR(300),
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    imagen_url VARCHAR(500) NULL,
    FOREIGN KEY (categorias_id) REFERENCES Categorias(categorias_id) ON DELETE RESTRICT
);

-- TABLA: Servicios
CREATE TABLE IF NOT EXISTS Servicios (
    servicio_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(20) NOT NULL DEFAULT 'habilitado' CHECK (estado IN ('habilitado', 'deshabilitado'))
);

-- TABLA: Reservas
CREATE TABLE IF NOT EXISTS Reservas (
    reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL,
    email VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(12) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    cantidad_personas INT NOT NULL CHECK (cantidad_personas > 0),
    comentario VARCHAR(300),
    estado VARCHAR(30) NOT NULL DEFAULT 'reservada' CHECK (estado IN ('reservada', 'cancelada', 'finalizada'))
    );

-- TABLA: Resenas
CREATE TABLE IF NOT EXISTS Resenas (
    resena_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL UNIQUE,
    puntuacion_ambiente INT NOT NULL CHECK (puntuacion_ambiente BETWEEN 1 AND 5),
    puntuacion_servicio INT NOT NULL CHECK (puntuacion_servicio BETWEEN 1 AND 5),
    puntuacion_comida INT NOT NULL CHECK (puntuacion_comida BETWEEN 1 AND 5),
    comentario TEXT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'habilitada' CHECK (estado IN ('habilitada', 'deshabilitada')),
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE
);

-- TABLA: Servicios_reserva
CREATE TABLE IF NOT EXISTS Servicios_reserva (
    servicios_reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL,
    servicio_id INT NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES Reservas(reserva_id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id) ON DELETE RESTRICT
);

-- TABLA: Mesas
CREATE TABLE IF NOT EXISTS Mesas (
    mesa_id INT PRIMARY KEY AUTO_INCREMENT,
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('ocupada', 'desocupada')),
    cantidad_mesas INT NOT NULL CHECK (cantidad_mesas >= 0)
);